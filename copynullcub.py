"""
Copy ISIS CUB(s) from cubsources/ to gittests/, with image data zeroed out

Usage:  python ./copynullcub.py cubsources/*.cub

"""
import os
import sys

if "__main__" == __name__:
  # Get source and destination sub-directory names
  dnSource, dnDest = 'cubsources gittests'.split()

  # Loop over input files
  for fnCubSource in sys.argv[1:]:

    try:

      # Don't process files from any sub-directory other than source
      dn,bn = os.path.split(fnCubSource)
      if dn != dnSource: continue

      # Open CUB
      with open(fnCubSource,'rb') as fIn:

        # Initial empty list of NNNs from [StartByte = NNN] lines
        startBytes = []

        # Add NNN values to list
        for pvlLine in fIn:
          toks = pvlLine.split()
          if len(toks) == 1 and toks[0]=='End': break
          if len(toks) == 3 and toks[0]=='StartByte': startBytes.append(int(toks[2]))
        
        # Ensure at least two StartByte entries
        assert startBytes > 1

        # Reset read pointer to start of file
        fIn.seek(0,0)
        assert fIn.tell() == 0

        # Sort startByte values
        startBytes.sort()

        # Assume first StartByte value is end of PVL and start of image data
        # Assume second StartByte value is end of image data
        endLbl, endImg = startBytes[:2]

        # Open output file in gittests/
        with open(os.path.join(dnDest,bn),'wb') as fOut:

          # Initialize current pointer
          currPos = 1

          ### Copy label from first (endLbl-1) bytes
          while currPos < endLbl:
            readData = fIn.read(endLbl-currPos)
            assert readData
            fOut.write(readData)
            currPos += len(readData)

          ### Use 64k buffer
          buffSize = 65536

          ### Write nulls for image, from endLbl to (endImg-1)
          zeros = '\0' * buffSize
          while currPos < (endImg-buffSize):
            fOut.write(zeros)
            currPos += buffSize
          fOut.write(zeros[:endImg-currPos])
          currPos += (endImg - currPos)
          assert currPos == endImg

          ### Write rest of file
          fIn.seek(endImg-1,0)
          readData = fIn.read(buffSize)
          while readData:
            fOut.write(readData)
            readData = fIn.read(buffSize)

      print('Copied CUB {}'.format(fnCubSource))

    except:
      import traceback
      traceback.print_exc()
      sys.stderr.write('### FAILED TO COPY {}\n'.format(fnCubSource))
