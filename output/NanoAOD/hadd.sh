OUTPUT_DIR="/eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD"
kappa_strings=("c3_0_d4_99" "c3_0_d4_0" "c3_0_d4_m1" "c3_19_d4_19" "c3_1_d4_0" "c3_1_d4_2" "c3_2_d4_m1" "c3_4_d4_9" "c3_m1_d4_0" "c3_m1_d4_m1" "c3_m1p5_d4_m0p5")
# kappa_strings=("c3_2_d4_m1")


for str in "${kappa_strings[@]}"; do

    hadd -f $OUTPUT_DIR/${str}.root $OUTPUT_DIR/${str}_2016.root $OUTPUT_DIR/${str}_2016APV.root $OUTPUT_DIR/${str}_2017.root $OUTPUT_DIR/${str}_2018.root
done


# OUTPUT_DIR="$INPUT_DIR/merged"
# FINAL_OUTPUT_FILE="$OUTPUT_DIR/nano_merged_final.root"

# # 创建输出目录
# mkdir -p $OUTPUT_DIR

# # 合并文件到四个部分
# hadd -f $OUTPUT_DIR/nano_merged_part1.root $INPUT_DIR/nano_1.root $INPUT_DIR/nano_1-1.root $INPUT_DIR/nano_1-2.root $INPUT_DIR/nano_1-3.root $INPUT_DIR/nano_1-4.root $INPUT_DIR/nano_1-5.root $INPUT_DIR/nano_3.root
# hadd -f $OUTPUT_DIR/nano_merged_part2.root $INPUT_DIR/nano_4.root $INPUT_DIR/nano_5.root $INPUT_DIR/nano_6.root $INPUT_DIR/nano_7.root
# hadd -f $OUTPUT_DIR/nano_merged_part3.root $INPUT_DIR/nano_8.root $INPUT_DIR/nano_10.root $INPUT_DIR/nano_11.root
# hadd -f $OUTPUT_DIR/nano_merged_part4.root $INPUT_DIR/nano_12.root $INPUT_DIR/nano_13.root $INPUT_DIR/nano_14.root $INPUT_DIR/nano_15.root $INPUT_DIR/nano_16.root $INPUT_DIR/nano_17.root

# # 合并四个部分为最终文件
# hadd -f $FINAL_OUTPUT_FILE $OUTPUT_DIR/nano_merged_part1.root $OUTPUT_DIR/nano_merged_part2.root $OUTPUT_DIR/nano_merged_part3.root $OUTPUT_DIR/nano_merged_part4.root

# # 输出合并完成信息
# echo "All files have been successfully merged into $FINAL_OUTPUT_FILE"

# python3 plot_gen_NanoAOD_root.py -s /eos/cms/store/group/phys_higgs/cmshhh/NanoAODv9PNetAK4/output_2017/HHHTo6B_c3_0_d4_99_TuneCP5_13TeV_amcatnlo-pythia8/NanoAODv9_ParticleNetAK4_RunIISummer20UL17MiniAODv2-106X_v9-v2/240220_104203/0000/@ -d /eos/user/x/xgeng/workspace/HHH/CMSSW_12_5_2/src/hhh-analysis-framework/output/NanoAOD -t c3_0_d4_99