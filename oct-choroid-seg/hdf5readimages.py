import sys
import os
import getopt
import imageio
import numpy as np
import h5py


def main(argv):
    infile = ""
    outpath = ""
    all = 0
    helpstr = "hdf5readimages.py -i <inputfile> -o <outputpath>\nUse -a to write all non-image content to a text file"
    # Example: python hdf5readimages.py -i example_data.hdf5 -o /usr/xyz/data/
    try:
        opts, args = getopt.getopt(argv, "hai:o:", ["ifile=", "opath="])

        for opt, arg in opts:
            if opt == "-h":
                print(helpstr)
                sys.exit()
            if opt == "-a":
                all = 1                
            elif opt in ("-i", "--ifile"):
                infile = arg
            elif opt in ("-o", "--opah"):
                outpath = arg
    except getopt.GetoptError:
        print(helpstr)
        sys.exit(2)
    if infile == "" or outpath == "":
        print(helpstr)
        sys.exit(2)

    f = h5py.File(infile, "r")

    # Extract keyes

    keys = list(f.keys())

    outfile = os.path.join(outpath, "hdf5imginfo.txt")
    ffile = open(outfile, "w+")

    for k in keys:
        print(k)
        ffile.write(k + "\n")
        kname = str(k)
        imgstr = "images"

        dset = f[kname][:]
        dims = dset.ndim
        print("Dims: " + str(dset.shape))
        content = str("Dims: " + str(dset.shape) + "\n")
        ffile.write(content)

        # Assume 4th dimension are RGB channels
        if dims == 4:
            dset1 = np.squeeze(dset)
            dims = dset1.ndim

        if dims == 3:  
            row, col, third = dset1.shape
            for x in range(0, row):
                data = np.array(dset1[:, :][x])
                # Extract images

                if imgstr in kname:
                    file = kname + str(x) + ".jpg"  # also png
                    file = os.path.join(outpath, file)
                    imageio.imwrite(file, data)

                # Extract segmentations/labels

                else:

                    segfile = kname + "_format" + str(x) + ".txt"
                    segfile = os.path.join(outpath, segfile)
                    file1 = open(segfile, "w+")
                    content = str(data)
                    file1.write(content)
                    file1.close()

                    if all == 1:
                        segfile = kname + "_all" + str(x) + ".txt"
                        segfile = os.path.join(outpath, segfile)
                        file1 = open(segfile, "w+")

                        file1.write(','.join(repr(item) for item in data))
                        file1.close()

    ffile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
