import sys
import os
import getopt
import imageio
import numpy as np
import h5py


def main(argv):
    infile = ""
    outpath = ""
    # Example: 'python hdf5readimages.py -i example_data.hdf5 -o /Users/xyz/data/
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "opath="])

        for opt, arg in opts:
            if opt == "-h":
                print("hdf5readimages.py -i <inputfile> -o <outputpath>")
                sys.exit()
            elif opt in ("-i", "--ifile"):
                infile = arg
            elif opt in ("-o", "--opah"):
                outpath = arg
    except getopt.GetoptError:
        print("hdf5readimages.py -i <inputfile> -o <outputpath>")
        sys.exit(2)
    if infile == "" or outpath == "":
        print("hdf5readimages.py -i <inputfile> -o <outputpath>")
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
        segstr = "segs"

        # Extract images

        if imgstr in kname:
            dset = f[kname][:]
            dims = dset.ndim
            print("Dims: " + str(dset.shape))
            content = str("Dims: " + str(dset.shape) + "\n")
            ffile.write(content)

            dset1 = np.squeeze(dset)
            dims = dset1.ndim

            if dims == 3:  # Check: 3 dims for images
                row, col, third = dset1.shape
                for x in range(0, row):
                    file = kname + str(x) + ".jpg"  # also png
                    file = os.path.join(outpath, file)

                    data = np.array(dset1[:, :, :][x])
                    imageio.imwrite(file, data)

        # Extract segmentations/labels

        elif segstr in kname:
            dset = f[kname][:]
            dims = dset.ndim
            print("Dims: " + str(dset.shape))
            content = str("Dims: " + str(dset.shape) + "\n")
            ffile.write(content)

            if dims == 3:  # Check: 3 dims for segs without squeeze
                row, col, third = dset.shape
                for x in range(0, row):
                    file = kname + str(x) + ".txt"

                    data = np.array(dset[:, :][x])

                    segformat = kname + "format" + str(x) + ".txt"
                    segformat = os.path.join(outpath, segformat)
                    file1 = open(segformat, "w+")

                    # Saving the 2D array in a text file

                    content = str(data)
                    file1.write(content)
                    file1.close()

    ffile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
