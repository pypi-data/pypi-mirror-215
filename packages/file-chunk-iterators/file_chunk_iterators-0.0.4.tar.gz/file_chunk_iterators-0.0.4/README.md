# file_chunk_iterators

Python classes to iterate through files in chunks


## Installation

pip install file_chunk_iterators


## Usage
We provide two functions:

1. iterate_file_in_chunks
   Iterator to iterate over chunks of a file.
   The iterator is initialized to specify how many lines/chunks to make.
   It is then used as iterator several times: each time, it will iterate over the lines of one chunk only.

2. iterate_file_in_chunks_with_key
   Iterate through a file in chunks, keeping together certain groups of lines defined by a key.
   This iterator class operates like iterate_file_in_chunks (see its docstring) but with an additional constraint:
   Here, lines in the file are characterized by a key. Consecutive lines with the same key can never be split to different chunks.
  

These methods can be used in conjuction with pandas.read_csv to read a pandas dataframe one chunk at the time, which may save memory.

Here below, you have the docstrings of the two methods:

```
iterate_file_in_chunks(fname, nlines=None, nchunks=None):
    Arguments:
      fname:   file to be opened
      nlines:  max number of lines per chunk
      nchunks: number of chunks (overrides nlines)

    Boolean attribute self.finished tells  whether the whole file has been iterated through

    Example #1: specifying number of lines
    ======================================
      iterator=iterate_file_in_chunks(fname, nlines=4)

      # first time: iterates over lines 1-4
      for line in iterator:        print (line)

      # 2nd time: iterates over lines 5-8
      for line in iterator:        print (line)

      # etc

    Example #2: specifying number of lines, iterate whole file
    ==========================================================
      iterator=iterate_file_in_chunks(fname, nlines=4)
      chunkindex=0  #optionally, keeping track of chunkindex
      while not iterator.finished:
        for line in iterator:
          print(line)
        chunkindex+=1


    Example #3: specifying number of chunks
    =======================================
      iterator=iterate_file_in_chunks(fname, nchunks=3)
      for chunkindex in range(nchunks):
        for line in iterator:
          print(line)

    Argument nchunks will estimate the nlines per chunk from the size of the file.
    Note, lines are never divided in subfractions; so if you divide a 10-line file in 3, you have
    chunk1= 4 lines       chunk2= 3 lines        chunk3= 3 lines

    How to use in pandas
    ====================
    This code was written specifically to read tabular files in chunks to use in pandas.
    Theoretically this is accomplished by pandas.read_csv(.. , chunksize=50), but in practice that will crash with certain files.
    So to accomplish this, use:

    nchunks=4
    iterator=iterate_file_in_chunks(fname, nchunks=nchunks)

    # determine column names somehow, e.g. with:
    with open(fname) as fh:
      colnames=fh.readline().strip().split('\t')

    for chunkindex in range(nchunks):
      # read a chunk of lines as dataframe
      chunkdf=pd.read_csv(iterator, engine='python', names=colnames, sep='\t',
                          header=(1 if chunkindex==0 else None) )

      # use chunkdf somehow, to obtain resdf
      resdf=process(chunkdf)

      # write all resdf to a file called outfile, one chunk at the time
      resdf.to_csv(outfile, sep='\t', index=False, header=(chunkindex == 0),
                mode=('w' if chunkindex == 0 else 'a') )

    Warning
    =======
     pandas.read_csv has unexpected behavior when nlines is small, say <3
     It will ignore some stopiterations, and concatenate what are supposed to be different chunks

     pandas version tested 1.3.3

```


```
iterate_file_in_chunks_with_key(fname, nlines, keyfn=lambda x:x[:x.index('\t')]):

    Arguments:
      fname:   file to be opened
      nlines:  max number of lines per chunk
      keyfn:   function to be applied to each line to derive its key  (default: get first tab-separated field)

    Note:
      - the chunk may have size greater than nlines if there are more than nlines consecutive lines with the same key
      - the same-key condition is tested only for consecutive lines

    Boolean attribute self.finished tells whether the whole file has been iterated through

    Example #1: specifying number of lines
    ======================================
      iterator=iterate_file_in_chunks_with_key(fname, nlines=10, keyfn=lambda x:x.split()[0])

      # first time: iterates over lines 1-4
      for line in iterator:        print (line)

      # 2nd time: iterates over lines 5-8
      for line in iterator:        print (line)

      # etc

    Example #2: specifying number of lines, iterate whole file
    ==========================================================
      iterator=iterate_file_in_chunks_with_key(fname, nlines=10, keyfn=lambda x:x.split()[0])
      chunkindex=0  #optionally, keeping track of chunkindex
      while not iterator.finished:
        for line in iterator:
          print(line)
        chunkindex+=1

    Warning
    =======
     pandas.read_csv has unexpected behavior when nlines is small, say <3
     It will ignore some stopiterations, and concatenate what are supposed to be different chunks

     pandas version tested 1.3.3
```
     



