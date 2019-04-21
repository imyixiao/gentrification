import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd


roc_1 = "../data/roc_1_lr.csv"
roc_2 = "../data/roc_2_lr.csv"
roc_3 = "../data/roc_3_lr.csv"


def grid_visual():
    classifier = ["Logistic Regression on Test", "Logistic Regression on Train", "SVC on Test",
            "SVC on Train", "Random Forest on Test", "Random Forest on Train"]
    definition = ["income_homeval_educ_pooling", "income_homeval_educ_unpooling", "income_homeval_pooling", "income_homeval_unpooling",
                "homeval_pooling", "homeval_unpooling"]

    res = np.array([[0.57, 0.62, 0.51, 0.60, 0.47, 0.00],
                    [0.54, 0.69, 0.53, 0.66, 0.52, 0.00],
                    [0.49, 0.52, 0.51, 0.53, 0.50, 0.51],
                    [0.55, 0.53, 0.50, 0.56, 0.50, 0.54],
                    [0.53, 0.50, 0.52, 0.50, 0.51, 0.50],
                    [0.71, 0.50, 0.65, 0.50, 0.65, 0.50]])


    fig, ax = plt.subplots()
    im = ax.imshow(res)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(definition)))
    ax.set_yticks(np.arange(len(classifier)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(definition)
    ax.set_yticklabels(classifier)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(classifier)):
        for j in range(len(definition)):
            text = ax.text(j, i, res[i, j],
                        ha="center", va="center", color="w")

    ax.set_title("Prediction Results(AUC) on Different Definitions, Classifers, Pooling Ways")
    fig.tight_layout()
    plt.show()



def feature_importance():
    res = {2: 0.0078, 4: 0.0116, 6: 0.0008, 7: 0.0017, 9: 0.0139, 12: 0.0042, 13: 0.0056, 15: 0.0022, 17: 0.0235, 18: 0.0031, 23: 0.0025, 25: 0.0289, 32: 0.0022, 35: 0.0003, 38: 0.0104, 51: 0.0073, 53: 0.0001, 56: 0.0018, 61: 0.001, 90: 0.0036, 94: 0.0014, 103: 0.0048, 112: 0.001, 130: 0.0041, 137: 0.002, 152: 0.0022, 165: 0.0066, 168: 0.0013, 179: 0.0014, 204: 0.001, 236: 0.0013, 253: 0.0006, 267: 0.0022, 273: 0.0012, 275: 0.001, 291: 0.0013, 293: 0.0026, 297: 0.0021, 306: 0.0006, 317: 0.0002, 331: 0.0, 342: 0.0124, 348: 0.0018, 363: 0.0021, 373: 0.0026, 393: 0.0023, 395: 0.0029, 400: 0.0087, 429: 0.0008, 466: 0.0132, 471: 0.0031, 522: 0.0016, 558: 0.0013, 559: 0.001, 560: 0.0045, 576: 0.0018, 585: 0.0102, 609: 0.0025, 626: 0.0067, 637: 0.0022, 669: 0.007, 753: 0.0055, 768: 0.0288, 779: 0.0029, 795: 0.0094, 801: 0.0011, 812: 0.0025, 823: 0.0558, 839: 0.0007, 862: 0.0152, 958: 0.0018, 1046: 0.0026, 1061: 0.0091, 1079: 0.0004, 1093: 0.0084, 1098: 0.0009, 1110: 0.0016, 1135: 0.0034, 1152: 0.008, 1194: 0.0018, 1237: 0.0007, 1290: 0.0167, 1328: 0.0044, 1333: 0.0028, 1370: 0.0022, 1409: 0.0013, 1417: 0.0039, 1438: 0.0236, 1439: 0.0011, 1464: 0.0031, 1526: 0.0013, 1538: 0.0011, 1587: 0.0013, 1685: 0.0013, 1695: 0.0013, 1702: 0.0011, 1722: 0.0018, 1743: 0.001, 1787: 0.0038, 1894: 0.002, 1996: 0.0021, 2232: 0.0199, 2341: 0.0029, 2364: 0.0065, 2490: 0.0632, 2595: 0.0061, 2599: 0.0103, 2794: 0.0006, 2823: 0.0032, 2826: 0.0025, 2917: 0.001, 2962: 0.0053, 2963: 0.0107, 3044: 0.0321, 3047: 0.0011, 3057: 0.0022, 3142: 0.0019, 3184: 0.0097, 3247: 0.005, 3505: 0.0, 3509: 0.0043, 3545: 0.0053, 3614: 0.0012, 3633: 0.0045, 3661: 0.001, 3698: 0.0037, 3794: 0.0203, 3820: 0.0239, 3912: 0.001, 4123: 0.0014, 4179: 0.0049, 4181: 0.0014, 4418: 0.0035, 4443: 0.003, 4506: 0.0012, 4525: 0.0196, 4546: 0.0072, 4559: 0.0007, 4859: 0.0103, 4966: 0.0262, 5082: 0.0023, 5256: 0.0048, 5269: 0.0179, 5406: 0.0039, 5421: 0.005, 5483: 0.0023, 5639: 0.0035, 5644: 0.0034, 5688: 0.0039, 5772: 0.0022, 5789: 0.0023, 5862: 0.0022, 6202: 0.0044, 6231: 0.0074, 6487: 0.0022, 6543: 0.003, 6563: 0.0058, 6577: 0.0028, 7033: 0.0055, 7123: 0.0053, 7166: 0.0105, 7519: 0.0026, 7796: 0.0021, 7849: 0.0017, 8049: 0.0027, 8119: 0.0046, 8145: 0.0027, 8272: 0.0068, 8283: 0.0032, 8441: 0.0026, 8814: 0.0013, 9431: 0.0034, 9694: 0.0057, 9773: 0.0325, 9823: 0.0007}
    ids = [0, 1, 2, 3, 4, 5, 10027]
    for id in ids:
        try:
            print(res[id])
        except:
            print("nothing find for " + str(id))


def roc_curve(roc_dict):
    plt.title('Receiver Operating Characteristic')
    for k,v in roc_dict.items():
        plt.plot(v['FPR'], v['TPR'], color=v['color'], linestyle=v['line'], label = "Def "+ k + "(area = " + v['roc'] + ")")
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'-')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


if __name__ == "__main__":
    roc_dict = dict()
    roc_dict["income_homeval_educ_pooling"] = dict()
    roc_dict["income_homeval_pooling"] = dict()
    roc_dict["homeval_pooling"] = dict()

    roc_3_df = pd.read_csv(roc_3)
    #darkgreen
    roc_dict["income_homeval_educ_pooling"]['color'] = '#006400' 
    roc_dict["income_homeval_educ_pooling"]['line'] = '--'
    roc_dict["income_homeval_educ_pooling"]['roc'] = '0.57'
    roc_dict["income_homeval_educ_pooling"]['FPR'] = roc_3_df['FPR'].tolist()
    roc_dict["income_homeval_educ_pooling"]['TPR'] = roc_3_df['TPR'].tolist()

    roc_2_df = pd.read_csv(roc_2)
    #lime
    roc_dict["income_homeval_pooling"]['color'] = '#00FF00'
    roc_dict["income_homeval_pooling"]['line'] = '--'
    roc_dict["income_homeval_pooling"]['roc'] = '0.51'
    roc_dict["income_homeval_pooling"]['FPR'] = roc_2_df['FPR'].tolist()
    roc_dict["income_homeval_pooling"]['TPR'] = roc_2_df['TPR'].tolist()

    roc_1_df = pd.read_csv(roc_1)
    #seagreen
    roc_dict["homeval_pooling"]['color'] = '#2E8B57'
    roc_dict["homeval_pooling"]['line'] = '--'
    roc_dict["homeval_pooling"]['roc'] = '0.47'
    roc_dict["homeval_pooling"]['FPR'] = roc_1_df['FPR'].tolist()
    roc_dict["homeval_pooling"]['TPR'] = roc_1_df['TPR'].tolist()

    '''
    to add more roc curve lines, just add here and rerun function
    '''
    
    roc_curve(roc_dict)