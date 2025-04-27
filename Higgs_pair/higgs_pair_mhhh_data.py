import ROOT
import math
from array import array

# 定义四矢量构建函数

class JetObject:
    def __init__(self, pt=0, eta=0, phi=0, mass=0, btagPNetB=0):
        # 初始化 JetObject 的属性
        self.pt = pt
        self.eta = eta
        self.phi = phi
        self.mass = mass

def polarP4(obj=None, pt='pt', eta='eta', phi='phi', mass='mass'):
    if obj is None:
        return ROOT.Math.PtEtaPhiMVector()
    pt_val = getattr(obj, pt) if pt else 0
    eta_val = getattr(obj, eta) if eta else 0
    phi_val = getattr(obj, phi) if phi else 0
    mass_val = getattr(obj, mass) if mass else 0
    return ROOT.Math.PtEtaPhiMVector(pt_val, eta_val, phi_val, mass_val)

# 定义 ΔR 计算函数
def deltaR2(eta1, phi1, eta2=None, phi2=None):
    if eta2 is None:
        a, b = eta1, phi1
        return deltaR2(a.eta, a.phi, b.eta, b.phi)
    else:
        deta = eta1 - eta2
        dphi = math.atan2(math.sin(phi1 - phi2), math.cos(phi1 - phi2))
        return deta * deta + dphi * dphi

def deltaR(eta1, phi1, eta2=None, phi2=None):
    return math.sqrt(deltaR2(eta1, phi1, eta2, phi2))

# 定义手动组合函数
def manualPermutation(input1, input2, input3=[0]):
    output = []
    for i1, v1 in enumerate(input1):
        for i2, v2 in enumerate(input2):
            if v1==v2 or (input1==input2 and i2<=i1): continue
            if v1.startswith("JP") and v2.startswith("JP") and len(list(set(v1.split("_")[1:]+v2.split("_")[1:])))<4: continue

            for i3, v3 in enumerate(input3):
                if v3 != 0:
                    if v1==v3 or (input1==input3 and i3<=i1): continue
                    if v2==v3 or (input2==input3 and i3<=i2): continue
                    if v1.startswith("JP") and v3.startswith("JP") and len(list(set(v1.split("_")[1:]+v3.split("_")[1:])))<4: continue
                    if v2.startswith("JP") and v3.startswith("JP") and len(list(set(v2.split("_")[1:]+v3.split("_")[1:])))<4: continue

                    output.append([v1, v2, v3])
                else:
                    output.append([v1, v2])
    return output

# 主函数，进行 Higgs 配对
def higgsPairing(jets_4vec, fatjets, XbbWP, Run=2):
    # 筛选符合条件的 fatjets
    probejets = sorted([fj for fj in fatjets if fj.Xbb > XbbWP], key=lambda x: x.Xbb, reverse=True)
    # print("Jets and Fatjets:")
    # for jet in jets_4vec:
    #     print(f"Jet: pt={jet.Pt()}, eta={jet.Eta()}, phi={jet.Phi()}, mass={jet.M()}, PNetB={jet.btagPNetB}")
    # for fatjet in fatjets:
    #     print(f"FatJet: pt={fatjet.Pt()}, eta={fatjet.Eta()}, phi={fatjet.Phi()}, mass={fatjet.M()}, Xbb={fatjet.Xbb}")


    # 创建 jet 配对
    jetpairs = []
    for i1, j1 in enumerate(jets_4vec):
        for i2, j2 in enumerate(jets_4vec):
            if i2 <= i1: continue
            jetpairs.append((i1, i2, j1 + j2, j1.btagPNetB * j2.btagPNetB, "Jet", (j1 + j2).M()))
    jetpairs = sorted([p for p in jetpairs], key=lambda x: x[3], reverse=True)

    # 构建 allobjects 字典，用于保存所有组合
    allobjects = {}
    for i, fj in enumerate(probejets):
        allobjects["FJ" + str(i + 1)] = fj
    for i, j in enumerate(jetpairs):
        allobjects["JP_" + str(j[0] + 1) + "_" + str(j[1] + 1)] = j

    # 获取符合条件的 jet 对象
    objlist_jet = [k for k in allobjects if "J" in k]

    # if entry_num % 1000 == 0:
        # print("All objects:")
        # for key, obj in allobjects.items():
        #     if key.startswith("FJ"):  # jet pair
        #         print(f"{key}: mass={obj.M()}, pt={obj.Pt()}, eta={obj.Eta()}, phi={obj.Phi()}")
        #     else:  # fatjet
        #         print(f"{key}: mass={obj[5]}, pt={obj[2].Pt()}, eta={obj[2].Eta()}, phi={obj[2].Phi()},PNetB={obj[3]}")



    # 生成可能的组合
    permutations = manualPermutation(objlist_jet, objlist_jet, objlist_jet)
    if not permutations:
        permutations = manualPermutation(objlist_jet, objlist_jet)
    if not permutations and len(objlist_jet) >= 1:
        permutations = [[obj] for obj in objlist_jet]

    # 设置 Higgs 数量
    nHiggs = len(permutations[0])

    # 初始化 Higgs 和 jet 容器
    h = [polarP4() for _ in range(3)]
    j = [polarP4() for _ in range(6)]

    # 寻找 chi2 最小的组合
    min_chi2 = 10000000000.0
    for permutation in permutations:
        masses = []
        for name in permutation:
            thismass = allobjects[name].M() if name.startswith("F") else allobjects[name][5]
            masses.append(thismass)
        fitted_mass = sum(masses) / nHiggs
        # print(permutation)
        # print(fitted_mass)
        # print("nHiggs")
        # print(nHiggs)
  
        chi2 = 0.0
        for m in masses:
            chi2 += (m - fitted_mass)**2
        # print(chi2)
        if chi2 < min_chi2:
            m_fit = fitted_mass
            min_chi2 = chi2
            finalPermutation = permutation
        if nHiggs==1: break
        # 更新最优组合
    # print(permutations[:10])

    # print(finalPermutation)

    # 填充 Higgs 对象的属性
    for i, name in enumerate(finalPermutation):
        if name.startswith("F"):
            h[i] = allobjects[name]
            h[i].Mass = h[i].M()
            h[i].pt = h[i].Pt() 
            h[i].eta = h[i].Eta()
            h[i].phi = h[i].Phi() 
        else:
            h[i] = allobjects[name][2]
            h[i].Mass = allobjects[name][5]
            h[i].pt = h[i].Pt()
            h[i].eta = h[i].Eta()
            h[i].phi = h[i].Phi()

    # 返回拟合质量和匹配的对象
    return m_fit, h[0], h[1], h[2], j[0], j[1], j[2], j[3], j[4], j[5]



# 1. 加载 ROOT 文件和树
path  = "/eos/cms/store/group/phys_higgs/cmshhh/v33/mva-inputs-2018-categorisation-spanet-boosted-classification/inclusive-weights"
output_path = "/eos/home-x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/categorization"
# year_list = ["2018","2017","2016","2016APV"]
year_list = ["2018"]
# cat_list = ["ProbHHH6b_3bh0h_inclusive_CR","ProbHHH6b_2bh1h_inclusive_CR","ProbHHH6b_1bh2h_inclusive_CR","ProbHHH6b_0bh3h_inclusive_CR"]
# cat_list = ["ProbHHH6b_3bh0h_inclusive_CR"]
file_list = ["JetHT"]
for year in year_list:
    for file in file_list:
        input_file = ROOT.TFile.Open("%s/%s.root"%(path,file), "READ")
        tree = input_file.Get("Events") 
        print ("processing: %s/%s.root"%(path,file)) # 替换为实际的树名

        # 创建输出文件并复制树结构
        output_file = ROOT.TFile("%s/%s/%s.root"%(output_path,year,file), "RECREATE")
        new_tree = tree.CloneTree(0)  # 创建空的树结构，不复制事件内容

        # 定义新的分支变量
        h_mass = array('f', [0.0])
        hhh_mass1 = array('f', [0.0])
        hhh_mass2 = array('f', [0.0])
        h1_pt = array('f', [0.0])
        h1_eta = array('f', [0.0])
        h1_phi = array('f', [0.0])
        h1_mass = array('f', [0.0])
        h2_pt = array('f', [0.0])
        h2_eta = array('f', [0.0])
        h2_phi = array('f', [0.0])
        h2_mass = array('f', [0.0])
        h3_pt = array('f', [0.0])
        h3_eta = array('f', [0.0])
        h3_phi = array('f', [0.0])
        h3_mass = array('f', [0.0])

        # 将新的分支添加到树中
        new_tree.Branch("h_mass", h_mass, "h_mass/F")
        new_tree.Branch("hhh_mass1", hhh_mass1, "hhh_mass1/F")
        new_tree.Branch("hhh_mass2", hhh_mass2, "hhh_mass2/F")
        new_tree.Branch("h1_pt", h1_pt, "h1_pt/F")
        new_tree.Branch("h1_eta", h1_eta, "h1_eta/F")
        new_tree.Branch("h1_phi", h1_phi, "h1_phi/F")
        new_tree.Branch("h1_mass", h1_mass, "h1_mass/F")
        new_tree.Branch("h2_pt", h2_pt, "h2_pt/F")
        new_tree.Branch("h2_eta", h2_eta, "h2_eta/F")
        new_tree.Branch("h2_phi", h2_phi, "h2_phi/F")
        new_tree.Branch("h2_mass", h2_mass, "h2_mass/F")
        new_tree.Branch("h3_pt", h3_pt, "h3_pt/F")
        new_tree.Branch("h3_eta", h3_eta, "h3_eta/F")
        new_tree.Branch("h3_phi", h3_phi, "h3_phi/F")
        new_tree.Branch("h3_mass", h3_mass, "h3_mass/F")

        # 2. 设置 b-tag 工作点
        XbbWP = 0.0 # 根据需要设置工作点

        # 3. 遍历每个事件，提取 jets 和 fatjets 信息
        total_entries = tree.GetEntries()
        for entry_num, event in enumerate(tree):
            if entry_num % 1000 == 0:
                print(f"Processing event {entry_num} / {total_entries}")

            # if entry_num  == 5:
            #     break

            jets_4vec = []
            for i in range(1, 11):  # 假设有 10 个 jet
                pt = getattr(event, f"jet{i}Pt")
                eta = getattr(event, f"jet{i}Eta")
                phi = getattr(event, f"jet{i}Phi")
                mass = getattr(event, f"jet{i}Mass")
                btagPNetB = getattr(event, f"jet{i}PNetB")

                if mass == 0.0:
                    continue
                # print("pt issss!!!!!!!!!!!!!!!!!!!")
                # print(pt)
                jet = JetObject()

                setattr(jet, "pt", pt)
                setattr(jet, "eta", eta)
                setattr(jet, "phi", phi)
                setattr(jet, "mass", mass)

                jet = polarP4(jet)
                setattr(jet, "btagPNetB", btagPNetB)  

                jets_4vec.append(jet)
            
            fatjets = []
            for i in range(1, 4):
                pt = getattr(event, f"fatJet{i}Pt")
                eta = getattr(event, f"fatJet{i}Eta")
                phi = getattr(event, f"fatJet{i}Phi")
                mass = getattr(event, f"fatJet{i}Mass")
                Xbb = getattr(event, f"fatJet{i}PNetXbb")
                fatjet = JetObject()

                setattr(fatjet, "pt", pt)
                setattr(fatjet, "eta", eta)
                setattr(fatjet, "phi", phi)
                setattr(fatjet, "mass", mass)

                fatjet = polarP4(fatjet)
                setattr(fatjet, "btagPNetB", btagPNetB) 

                setattr(fatjet, "Xbb", Xbb)  

                fatjets.append(fatjet)

            # 运行配对
            m_fit, h1, h2, h3, j1, j2, j3, j4, j5, j6 = higgsPairing(jets_4vec, fatjets, XbbWP)

            # 填充新分支的数据
            h_mass[0] = m_fit
            hhh_mass1[0] = m_fit*3
            hhh_mass2[0] = (h1+h2+h3).M()
            h1_pt[0] = h1.Pt()
            h1_eta[0] = h1.Eta()
            h1_phi[0] = h1.Phi()
            h1_mass[0] = h1.M()
            h2_pt[0] = h2.Pt()
            h2_eta[0] = h2.Eta()
            h2_phi[0] = h2.Phi()
            h2_mass[0] = h2.M()
            h3_pt[0] = h3.Pt()
            h3_eta[0] = h3.Eta()
            h3_phi[0] = h3.Phi()
            h3_mass[0] = h3.M()
            # if entry_num % 1000 == 0:
            #     print(f"h1: pt={h1.Pt()}, eta={h1.Eta()}, phi={h1.Phi()}, mass={h1.M()}")
            #     print(f"h2: pt={h2.Pt()}, eta={h2.Eta()}, phi={h2.Phi()}, mass={h2.M()}")
            #     print(f"h3: pt={h3.Pt()}, eta={h3.Eta()}, phi={h3.Phi()}, mass={h3.M()}")
            #     print(m_fit*3)
            #     print((h1+h2+h3).M())


            new_tree.Fill()

        print("Processing complete. Writing output to file.")

        output_file.Write()
        output_file.Close()
        input_file.Close()
