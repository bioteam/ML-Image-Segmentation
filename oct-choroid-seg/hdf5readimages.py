import sys, getopt
import imageio
import matplotlib.pyplot as plt
import matplotlib.image
import numpy as np
import h5py

def main(argv):
    infile = ''
    outfile = ''
    # Example: Run with 'python hdf5readimages.py -i example_data.hdf5 -o hdf5-format.txt'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])

        for opt, arg in opts:
            if opt == '-h':
                print('hdf5readimages.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                infile = arg
            elif opt in ("-o", "--ofile"):
                outfile = arg
    except getopt.GetoptError as e:
        print('hdf5readimages.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    if infile == '' or outfile == '':
        print('hdf5readimages.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
        
    f = h5py.File(infile)
    
    
    #Extract keyes

    keys = list(f.keys())
    print(keys)

    ffile = open(outfile, "w+")


    for k in keys:
        print(k)
        ffile.write(k+"\n")
        kname=str(k)
        imgstr='images'
        segstr='segs'

        #Extract images

        if imgstr in kname:   
            dset=f[kname][:]
            dims=dset.ndim
            print("Dims: " + str(dset.shape))
            content = str("Dims: " + str(dset.shape)+"\n")
            ffile.write(content)

            dset1=np.squeeze(dset)
            dims=dset1.ndim

            if (dims == 3): #Check: 3 dims for images
                row, col, third = dset1.shape
                for x in range(0,row):
                    file=kname+str(x)+'.jpg' #also png

                    
                    data=np.array(dset1[:,:,:][x])
                    drot90=np.rot90(data,3)
                    imageio.imwrite(file,drot90)

                    # Can also save image with matplotlib
                    #matplotlib.image.imsave(file, data)

        #Extract segmentations/labels

        elif segstr in kname:
            dset=f[kname][:]
            dims=dset.ndim
            print("Dims: " + str(dset.shape))
            content = str("Dims: " + str(dset.shape)+"\n")
            ffile.write(content)

            if (dims == 3): #Check: 3 dims for segs without squeeze
                row, col, third = dset.shape
                for x in range(0,row):
                    file=kname+str(x)+'.txt'

                    data=np.array(dset[:,:][x])
                    
                    #np.savetxt(file, data,fmt='%s')

                    segformat= kname+ 'format'+ str(x)+'.txt'
                    file1 = open(segformat, "w+")
    
                    # Saving the 2D array in a text file

                    content = str(data)
                    file1.write(content)
                    file1.close()

    ffile.close()

if __name__ == "__main__":
    main(sys.argv[1:])