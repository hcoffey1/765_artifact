#Used to provide the intial sizing values for the rough draft of the node link chart
import numpy as np

def main():
    ImgDim = 800
    CenterNodeSize = 150
    MaxEdgeLength = 285

    NodeSize = np.array([.4, 0.14, 0.16, 0.23, 0.07])

    Quantiles = [
            [.34, .39, .45, .71],
            [0, 0.04, 0.30, 0.56],
            [0.07, 0.14, 0.23, 0.51],
            [0.11, 0.20, 0.32, 0.63],
            [0.02, 0.05, 0.10, 0.34]
            ]
    
    print("Percentages")
    print(NodeSize)

    print("Node Pixel Sizes")
    NodeSizePercentages = (np.multiply(NodeSize, CenterNodeSize))
    print(np.around(NodeSizePercentages, decimals=0))

    print("Edge Pixel Lengths")
    EdgeLengthPercentages = (np.multiply(NodeSize, MaxEdgeLength))
    print(np.around(EdgeLengthPercentages, decimals=0))

    print("Edge tick lengths")

    Ticks = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    Ticks = np.multiply(Ticks, MaxEdgeLength)
    #print(Ticks)
    print(np.around(Ticks, decimals=0))

    print("Edge tick Position")
    Ticks =  np.multiply(Ticks, -1)
    Ticks = Ticks + ( (ImgDim/2) - (CenterNodeSize/2) )
    print(Ticks)
    
    print("Quantiles")
    i = 1
    for cat in Quantiles:
        print("Cat ", i)
        
        TmpArray = np.array(cat)
        
        TmpArray = (np.multiply(TmpArray, MaxEdgeLength))

        print(np.around(TmpArray, decimals=0))

        i+=1



if __name__ == "__main__":
    main()
