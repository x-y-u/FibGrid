

dataset_types = [
    "HCP72",
    "ORG_AnatomicalTracts",
    "Tracts39"
]


def get_bundle_names(dataset_type=0):
    bundles_0 = ['AF_left', 'AF_right', 'ATR_left', 'ATR_right', 'CA', 'CC_1', 'CC_2', 'CC_3', 'CC_4', 'CC_5', 'CC_6',
                 'CC_7', 'CG_left', 'CG_right', 'CST_left', 'CST_right', 'MLF_left', 'MLF_right', 'FPT_left',
                 'FPT_right', 'FX_left', 'FX_right', 'ICP_left', 'ICP_right', 'IFO_left', 'IFO_right', 'ILF_left',
                 'ILF_right', 'MCP', 'OR_left', 'OR_right', 'POPT_left', 'POPT_right', 'SCP_left', 'SCP_right',
                 'SLF_I_left', 'SLF_I_right', 'SLF_II_left', 'SLF_II_right', 'SLF_III_left', 'SLF_III_right',
                 'STR_left', 'STR_right', 'UF_left', 'UF_right', 'CC', 'T_PREF_left', 'T_PREF_right', 'T_PREM_left',
                 'T_PREM_right', 'T_PREC_left', 'T_PREC_right', 'T_POSTC_left', 'T_POSTC_right', 'T_PAR_left',
                 'T_PAR_right', 'T_OCC_left', 'T_OCC_right', 'ST_FO_left', 'ST_FO_right', 'ST_PREF_left',
                 'ST_PREF_right', 'ST_PREM_left', 'ST_PREM_right', 'ST_PREC_left', 'ST_PREC_right', 'ST_POSTC_left',
                 'ST_POSTC_right', 'ST_PAR_left', 'ST_PAR_right', 'ST_OCC_left', 'ST_OCC_right']

    bundles_1 = ['T_CB_right', 'T_Sup-T_right', 'T_TP_right', 'T_SLF-I_left', 'T_AF_right', 'T_Sup-OT_left',
                 'T_Sup-P_right', 'T_Sup-PO_left', 'T_SO_right', 'T_ILF_right', 'T_Intra-CBLM-I&P_left',
                 'T_AF_left', 'T_Sup-PO_right', 'T_Sup-O_right', 'T_CC7', 'T_Sup-P_left', 'T_EmC_right',
                 'T_CC3', 'T_MCP', 'T_EmC_left', 'T_TF_right', 'T_ICP_right', 'T_MdLF_right', 'T_SLF-II_right',
                 'T_SP_right', 'T_SLF-I_right', 'T_SF_right', 'T_SLF-II_left', 'T_IOFF_left', 'T_SF_left',
                 'T_PLIC_left', 'T_CR-F_left', 'T_EC_left', 'T_Sup-T_left', 'T_CPC_right', 'T_CC4',
                 'T_Sup-PT_left', 'T_TO_right', 'T_Intra-CBLM-I&P_right', 'T_SO_left', 'T_SLF-III_left',
                 'T_CR-P_right', 'T_CPC_left', 'T_PLIC_right', 'T_Sup-PT_right', 'T_TF_left', 'T_CR-P_left',
                 'T_CB_left', 'T_ICP_left', 'T_CST_left', 'T_CST_right', 'T_CR-F_right', 'T_UF_right', 'T_CC2',
                 'T_Sup-FP_right', 'T_IOFF_right', 'T_Sup-OT_right', 'T_MdLF_left', 'T_ILF_left', 'T_CC6',
                 'T_Intra-CBLM-PaT_right', 'T_TP_left', 'T_Sup-F_left', 'T_Sup-FP_left', 'T_CC5', 'T_TO_left',
                 'T_Sup-O_left', 'T_Sup-F_right', 'T_SLF-III_right', 'T_UF_left', 'T_Intra-CBLM-PaT_left',
                 'T_CC1', 'T_EC_right', 'T_SP_left']

    bundles_2 = ['ICP_R', 'SCP_R', 'SLF_L', 'MdLF_R', 'CC_Fr_2', 'CC_Pr_Po', 'AF_R',
                 'IFOF_R', 'PYT_R', 'OR_ML_L', 'FAT_L', 'CC_Oc', 'FX_L', 'SCP_L',
                 'CG_L', 'AF_L', 'ICP_L', 'CC_Pa', 'FAT_R', 'CC_Fr_1', 'OR_ML_R',
                 'UF_R', 'PC', 'IFOF_L', 'FPT_L', 'MdLF_L', 'FX_R', 'CG_R', 'AC',
                 'POPT_R', 'FPT_R', 'ILF_L', 'PYT_L', 'UF_L', 'POPT_L', 'MCP',
                 'CC_Te', 'ILF_R', 'SLF_R']
    if dataset_type == 0:
        return bundles_0
    elif dataset_type == 1:
        return bundles_1
    elif dataset_type == 2:
        return bundles_2


# HCP_105
# (bad subjects removed: 994273, 937160, 885975, 788876, 713239)
# (no CA: 885975, 788876, 713239)
all_subjects_FINAL = ["992774", "991267", "987983", "984472", "983773", "979984", "978578", "965771", "965367", "959574",
                    "958976", "957974", "951457", "932554", "930449", "922854", "917255", "912447", "910241", "907656",
                    "904044", "901442", "901139", "901038", "899885", "898176", "896879", "896778", "894673", "889579",
                    "887373", "877269", "877168", "872764", "872158", "871964", "871762", "865363", "861456", "859671",
                    "857263", "856766", "849971", "845458", "837964", "837560", "833249", "833148", "826454", "826353",
                    "816653", "814649", "802844", "792766", "792564", "789373", "786569", "784565", "782561", "779370",
                    "771354", "770352", "765056", "761957", "759869", "756055", "753251", "751348", "749361", "748662",
                    "748258", "742549", "734045", "732243", "729557", "729254", "715647", "715041", "709551", "705341",
                    "704238", "702133", "695768", "690152", "687163", "685058", "683256", "680957", "679568", "677968",
                    "673455", "672756", "665254", "654754", "645551", "644044", "638049", "627549", "623844", "622236",
                    "620434", "613538", "601127", "599671", "599469"]

