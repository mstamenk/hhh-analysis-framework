import ROOT
import math
from array import array
import time  # 新增导入

# 记录起始时间
start_time = time.time()

# # 定义四矢量构建函数
# class JetObject:
#     def __init__(self, pt=0, eta=0, phi=0, mass=0, btagPNetB=0):
#         self.pt = pt
#         self.eta = eta
#         self.phi = phi
#         self.mass = mass
#         self.btagPNetB = btagP


# # 定义四矢量构建函数
# class JetObject:
#     def __init__(self, pt=0, eta=0, phi=0, mass=0, btagPNetB=0):
#         self.pt = pt
#         self.eta = eta
#         self.phi = phi
#         self.mass = mass
#         self.btagPNetB = btagPNetB

# def polarP4(pt, eta, phi, mass):
#     return ROOT.Math.PtEtaPhiMVector(pt, eta, phi, mass)

# def deltaR2(eta1, phi1, eta2=None, phi2=None):
#     if eta2 is None:
#         a, b = eta1, phi1
#         return deltaR2(a.eta, a.phi, b.eta, b.phi)
#     else:
#         deta = eta1 - eta2
#         dphi = math.atan2(math.sin(phi1 - phi2), math.cos(phi1 - phi2))
#         return deta * deta + dphi * dphi

# def deltaR(eta1, phi1, eta2=None, phi2=None):
#     return math.sqrt(deltaR2(eta1, phi1, eta2, phi2))
#     # 注册 C++ 函数
    

# 使用 Define 调用 C++ 函数
#include <vector>
#include <string>
#include <set>
#include <sstream>
#include <algorithm>
ROOT.gInterpreter.Declare('''
    ROOT::Math::PtEtaPhiMVector polarP4(float pt, float eta, float phi, float mass) {
        return ROOT::Math::PtEtaPhiMVector(pt, eta, phi, mass);
    }

        // 辅助函数：将字符串按 '_' 分割为集合
    std::set<std::string> splitAndCollect(const std::string& str) {
        std::set<std::string> parts;
        size_t start = str.find('_') + 1;  // 从第一个下划线之后开始
        if (start == std::string::npos) return parts;  // 如果没有下划线，直接返回空集合

        std::istringstream stream(str.substr(start));
        std::string part;

        while (std::getline(stream, part, '_')) {
            parts.insert(part);
        }

        return parts;
    }
    # // 定义 Jet 结构体
    struct Jet {
        ROOT::Math::PtEtaPhiMVector fourVector;
        double PNetB;
    };

    // 定义 FatJet 结构体
    struct FatJet {
        ROOT::Math::PtEtaPhiMVector fourVector;
        double Xbb;
    };

    // 实现 manualPermutation 函数，保留功能与原 Python 代码一致
    std::vector<std::vector<std::string>> manualPermutation(
        const std::vector<std::string>& input1,
        const std::vector<std::string>& input2,
        const std::vector<std::string>& input3 = {"0"}
    ) {
        std::vector<std::vector<std::string>> output;

        for (size_t i1 = 0; i1 < input1.size(); ++i1) {
            const std::string& v1 = input1[i1];
            for (size_t i2 = 0; i2 < input2.size(); ++i2) {
                const std::string& v2 = input2[i2];
                if (v1 == v2 || (input1 == input2 && i2 <= i1)) continue;

                // 检查 JP 类型过滤条件
                if (v1.rfind("JP", 0) == 0 && v2.rfind("JP", 0) == 0) {
                    std::set<std::string> combined_parts = splitAndCollect(v1);
                    std::set<std::string> v2_parts = splitAndCollect(v2);
                    combined_parts.insert(v2_parts.begin(), v2_parts.end());
                    if (combined_parts.size() < 4) continue;
                }

                for (size_t i3 = 0; i3 < input3.size(); ++i3) {
                    const std::string& v3 = input3[i3];
                    if (v3 != "0") {
                        if (v1 == v3 || (input1 == input3 && i3 <= i1)) continue;
                        if (v2 == v3 || (input2 == input3 && i3 <= i2)) continue;

                        // 检查 JP 类型的继续条件
                        if (v1.rfind("JP", 0) == 0 && v3.rfind("JP", 0) == 0) {
                            std::set<std::string> combined_parts = splitAndCollect(v1);
                            std::set<std::string> v3_parts = splitAndCollect(v3);
                            combined_parts.insert(v3_parts.begin(), v3_parts.end());
                            if (combined_parts.size() < 4) continue;
                        }
                        if (v2.rfind("JP", 0) == 0 && v3.rfind("JP", 0) == 0) {
                            std::set<std::string> combined_parts = splitAndCollect(v2);
                            std::set<std::string> v3_parts = splitAndCollect(v3);
                            combined_parts.insert(v3_parts.begin(), v3_parts.end());
                            if (combined_parts.size() < 4) continue;
                        }

                        output.push_back({v1, v2, v3});
                    } else {
                        output.push_back({v1, v2});
                    }
                }
            }
        }

        return output;
    }

    #include <vector>
    #include <string>
    #include <set>
    #include <sstream>
    #include <algorithm>
    #include <map>
    #include <tuple>
    #include <limits>
    #include <cmath>
    #include <numeric>
    #include <iostream>
    #include "Math/Vector4D.h"  // 包含 ROOT 的四矢量类型定义
    #include <tuple> 

    



    // Higgs pairing 函数
    
    std::tuple<float, float, std::vector<std::tuple<float, float, float, float>>> higgsPairing(
        const std::vector<Jet>& jets_4vec,
        const std::vector<FatJet>& fatjets,
        float XbbWP,
        int Run = 2
    ) {
        // 筛选符合条件的 fatjets
        std::vector<FatJet> probejets;
        for (const auto& fj : fatjets) {
            if (fj.Xbb > XbbWP) probejets.push_back(fj);
        }
        std::sort(probejets.begin(), probejets.end(), [](const FatJet& a, const FatJet& b) {
            return a.Xbb > b.Xbb;
        });

        // 构建 jet pairs
        std::vector<std::tuple<int, int, ROOT::Math::PtEtaPhiMVector, float, std::string, float>> jetpairs;
        for (size_t i1 = 0; i1 < jets_4vec.size(); ++i1) {
            for (size_t i2 = i1 + 1; i2 < jets_4vec.size(); ++i2) {
                ROOT::Math::PtEtaPhiMVector sumVector = jets_4vec[i1].fourVector + jets_4vec[i2].fourVector;
                float score = jets_4vec[i1].PNetB * jets_4vec[i2].PNetB;
                jetpairs.emplace_back(i1, i2, sumVector, score, "Jet", sumVector.M());
            }
        }

        std::sort(jetpairs.begin(), jetpairs.end(), [](const auto& a, const auto& b) {
            return std::get<3>(a) > std::get<3>(b);
        });

        // 构建所有对象
        std::map<std::string, std::variant<decltype(jetpairs)::value_type, FatJet>> allobjects;
        for (const auto& p : jetpairs) {
            std::string name = "JP_" + std::to_string(std::get<0>(p) + 1) + "_" + std::to_string(std::get<1>(p) + 1);
            allobjects[name] = p;
        }
        for (size_t i = 0; i < probejets.size(); ++i) {
            allobjects["FJ" + std::to_string(i + 1)] = probejets[i];
        }

        // 获取对象列表并进行排列组合
        std::vector<std::string> objlist_jet;
        for (const auto& [key, _] : allobjects) {
            if (key.find("J") != std::string::npos) objlist_jet.push_back(key);
        }

        std::vector<std::vector<std::string>> permutations = manualPermutation(objlist_jet, objlist_jet, objlist_jet);
        if (permutations.empty()) {
            permutations = manualPermutation(objlist_jet, objlist_jet);
        }
        if (permutations.empty() && !objlist_jet.empty()) {
            permutations = {{objlist_jet[0]}};
        }

        // Chi2 计算和最终配对
        int nHiggs = permutations[0].size();
        float min_chi2 = std::numeric_limits<float>::infinity();
        std::vector<std::string> finalPermutation;
        float m_fit = 0.0;

        if (nHiggs <= 1) {
            return std::make_tuple(-1.0f, -1.0f, std::vector<std::tuple<float, float, float, float>>());
        }

        for (const auto& permutation : permutations) {
            std::vector<float> masses;
            for (const auto& name : permutation) {
                if (name.rfind("JP", 0) == 0) {
                    masses.push_back(std::get<5>(std::get<decltype(jetpairs)::value_type>(allobjects[name])));
                } else {
                    masses.push_back(std::get<FatJet>(allobjects[name]).fourVector.M());
                }
            }

            float avg_mass = std::accumulate(masses.begin(), masses.end(), 0.0f) / nHiggs;
            float chi2 = 0.0f;
            for (float mass : masses) {
                chi2 += std::pow(mass - avg_mass, 2);
            }

            if (chi2 < min_chi2) {
                min_chi2 = chi2;
                m_fit = avg_mass;
                finalPermutation = permutation;
            }
        }

        // 构建最终 Higgs 对象
        ROOT::Math::PtEtaPhiMVector hhh_sum_vector;
        std::vector<std::tuple<float, float, float, float>> finalHiggs;
        for (const auto& name : finalPermutation) {
            if (name.rfind("FJ", 0) == 0) {
                const auto& obj = std::get<FatJet>(allobjects[name]);
                finalHiggs.emplace_back(obj.fourVector.Pt(), obj.fourVector.Eta(), obj.fourVector.Phi(), obj.fourVector.M());
                hhh_sum_vector += obj.fourVector;  // 累加四矢量
            } else {
                const auto& obj = std::get<decltype(jetpairs)::value_type>(allobjects[name]);
                finalHiggs.emplace_back(std::get<2>(obj).Pt(), std::get<2>(obj).Eta(), std::get<2>(obj).Phi(), std::get<5>(obj));
                hhh_sum_vector += std::get<2>(obj);  // 累加四矢量
            }
        }

        float hhh_mass2 = hhh_sum_vector.M();
        return std::make_tuple(hhh_mass2, m_fit, finalHiggs);
    }
''')

# ROOT.gInterpreter.Declare('''
# struct Jet {
#     ROOT::Math::PtEtaPhiMVector fourVector;
#     float PNetB;
# };
# ''')






# 设置路径和文件信息
path = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-2018-categorisation-spanet-boosted-classification/inclusive-weights"
output_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/categorization"
year_list = ["2018"]
# file_list = ["QCD_datadriven"]
file_list = ["ZZTo4Q"]

for year in year_list:
    for file in file_list:
        input_file = ROOT.TFile.Open(f"{path}/{file}.root", "READ")
        tree = input_file.Get("Events")
        print(f"Processing: {path}/{file}.root")

        df = ROOT.RDataFrame(tree)


        # Python 生成 Define 表达式
        # define_jet = """
        #     struct Jet {
        #         ROOT::Math::PtEtaPhiMVector fourVector;
        #         float PNetB;
        #     };
        #     std::vector<Jet> jets;
        # """

        define_jet = """
            std::vector<Jet> jets;
        """

        for i in range(1, 11):
            define_jet += f"""
            if (jet{i}Mass > 0.0) {{
                jets.push_back({{ROOT::Math::PtEtaPhiMVector(jet{i}Pt, jet{i}Eta, jet{i}Phi, jet{i}Mass), jet{i}PNetB}});
            }}
            """

        define_jet += "return jets;"

        # 定义 RDataFrame
        df = df.Define("jets_4vec", define_jet)

        # 动态生成 fatjets_4vec 的 C++ 代码
        # define_fatjet = """
        #     struct FatJet {
        #         ROOT::Math::PtEtaPhiMVector fourVector;
        #         float Xbb;
        #     };
        #     std::vector<FatJet> fatjets;
        # """

        define_fatjet = """
            std::vector<FatJet> fatjets;
        """

        # 动态生成每个 fatJet 分支的代码
        for i in range(1, 4):  # 假设最多有 3 个 fatJet
            define_fatjet += f"""
            if (fatJet{i}Mass > 0.0) {{
                fatjets.push_back({{ROOT::Math::PtEtaPhiMVector(fatJet{i}Pt, fatJet{i}Eta, fatJet{i}Phi, fatJet{i}Mass), fatJet{i}PNetXbb}});
            }}
            """

        # 完成代码定义
        define_fatjet += "return fatjets;"

        # 定义 RDataFrame
        df = df.Define("fatjets_4vec", define_fatjet)
        total_events = df.Count().GetValue()
        print(f"total entries: {total_events}")

        # df = df.Define("higgs_info", "higgsPairing(jets_4vec, fatjets_4vec, 0.0)").Filter("higgs_info.first >= 0.0", "Skip invalid events")
        df = df.Define("higgs_info", "higgsPairing(jets_4vec, fatjets_4vec, 0.0)") \
            .Filter("std::get<0>(higgs_info) >= 0.0", "Skip invalid events")
        output_file = ROOT.TFile(f"{output_path}/{year}/{file}_new.root", "RECREATE")


        df = df.Define("hhh_mass2", "std::get<0>(higgs_info)") \
            .Define("hhh_mass1", "std::get<1>(higgs_info) *3") \
            .Define("h_mass", "std::get<1>(higgs_info)") \
            .Define("h1_pt", "std::get<0>(std::get<2>(higgs_info)[0])") \
            .Define("h1_eta", "std::get<1>(std::get<2>(higgs_info)[0])") \
            .Define("h1_phi", "std::get<2>(std::get<2>(higgs_info)[0])") \
            .Define("h1_mass", "std::get<3>(std::get<2>(higgs_info)[0])") \
            .Define("h2_pt", "std::get<0>(std::get<2>(higgs_info)[1])") \
            .Define("h2_eta", "std::get<1>(std::get<2>(higgs_info)[1])") \
            .Define("h2_phi", "std::get<2>(std::get<2>(higgs_info)[1])") \
            .Define("h2_mass", "std::get<3>(std::get<2>(higgs_info)[1])") \
            .Define("h3_pt", "std::get<0>(std::get<2>(higgs_info)[2])") \
            .Define("h3_eta", "std::get<1>(std::get<2>(higgs_info)[2])") \
            .Define("h3_phi", "std::get<2>(std::get<2>(higgs_info)[2])") \
            .Define("h3_mass", "std::get<3>(std::get<2>(higgs_info)[2])")

        original_branches = [branch.GetName() for branch in tree.GetListOfBranches()]

        branches_to_remove = ["jets_4vec", "fatjets_4vec", "higgs_info"]
        original_branches = [branch for branch in original_branches if branch not in branches_to_remove]

        # 定义其他需要保存的新 branch
        all_branches = original_branches + [
            "h_mass", "hhh_mass1", "hhh_mass2",
            "h1_pt", "h1_eta", "h1_phi", "h1_mass",
            "h2_pt", "h2_eta", "h2_phi", "h2_mass",
            "h3_pt", "h3_eta", "h3_phi", "h3_mass"
        ]
        def output_every_1000_entries(df):
            # 将 RDataFrame 转为 NumPy 数组字典
            data = df.AsNumpy(["hhh_mass2", "h_mass"])

            # 获取每列数据（每列长度相同）
            hhh_mass2_values = data["hhh_mass2"]
            h_mass_values = data["h_mass"]

            # 遍历每个事例，按索引输出
            for count, (hhh_mass2, h_mass) in enumerate(zip(hhh_mass2_values, h_mass_values)):
                if count % 1000 == 0:
                    print(f"Entry {count}: hhh_mass2 = {hhh_mass2}, h_mass = {h_mass}")

        # 使用 Snapshot 将所有分支批量写入新文件
        # all_branches = original_branches + [
        #     "h_mass","hhh_mass1","hhh_mass2", "h1_pt", "h1_eta", "h1_phi", "h1_mass",
        #     "h2_pt", "h2_eta", "h2_phi", "h2_mass",
        #     "h3_pt", "h3_eta", "h3_phi", "h3_mass"
        # ]

        # all_branches = [
        #     "h_mass","hhh_mass1","hhh_mass2", "h1_pt", "h1_eta", "h1_phi", "h1_mass",
        #     "h2_pt", "h2_eta", "h2_phi", "h2_mass",
        #     "h3_pt", "h3_eta", "h3_phi", "h3_mass"
        # ]
        # print(df.GetColumnNames())


        df.Snapshot("Events", f"{output_path}/{year}/{file}_new.root", all_branches)


        


        output_file.Write()
        output_file.Close()
        input_file.Close()

end_time = time.time()
elapsed_time = end_time - start_time
elapsed_minutes = elapsed_time / 60  # 将秒数转换为分钟
print(f"Total execution time: {elapsed_minutes:.2f} minutes")
