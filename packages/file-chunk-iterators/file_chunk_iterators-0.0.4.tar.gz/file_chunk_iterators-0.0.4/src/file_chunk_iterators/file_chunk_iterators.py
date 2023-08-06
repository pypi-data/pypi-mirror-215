
class iterate_file_in_chunks: 
    """ Iterator to iterate over chunks of a file. 
    The iterator is initialized to specify how many lines/chunks to make.
    It is then used as iterator several times: each time, it will iterate over the lines of one chunk only.

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

    """

    def __init__(self, fname, nlines=None, nchunks=None):
        self.fh=open(fname, 'r')
        self.totlines=buf_count_newlines_gen(fname)
        if not nchunks is None:
            self.chunksize=self.totlines/nchunks
        elif not nlines is None:
            self.chunksize=nlines
        else:
            raise Exception("ERROR you must specify nlines or nchunks")
        self.chunkindex=0
        self.globalindex=0
        self.finished=False
        
    def __iter__(self):    
        return self #.fh.__iter__()

    def __next__(self):
        if self.totlines==self.globalindex:
            self.finished=True
            #print('stop iteration for good')
            raise StopIteration
        
        if self.globalindex >= ( (self.chunkindex+1) * self.chunksize):
            #print('stop iteration chunk')           
            self.chunkindex+=1
            raise StopIteration
        
        self.globalindex+=1            
        return self.fh.__next__()

    # def get_next_lines(self, nlines=1):
    #     """ Returns a list of next nlines, whose number is counted towards the current chunk size 
    #         (wll never trigger a stop iteration because chunk is over, unless file is over)"""
    #     return [self.fh.__next__()  for _ in range(nlines)]           

    readline=__next__
    
    def read(self, size):
        ### necessary just so pandas accept this as valid IO buffer
        pass

class iterate_file_in_chunks_with_key:
    """Iterate through a file in chunks, keeping together certain groups of lines defined by a key.

This iterator class operates like iterate_file_in_chunks (see its docstring) but with an additional constraint:
Here, lines in the file are characterized by a key. Consecutive lines with the same key can never be split to different chunks.

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
    
    """
    
    def __init__(self, fname, nlines,
                 keyfn=lambda x:x[:x.index('\t')]):

        # self.fh will parse the file to determine keys
        # based on that, we keep track of how many lines needs to be returned any given moment through the vars further below
        self.fh= open(fname, 'r')

        # self.fh2 is the actual filehandler that returns the lines
        self.fh2=open(fname, 'r')

        ### deprecated
        # if not nchunks is None:
        #     totlines=buf_count_newlines_gen(fname)
        #     self.chunksize=totlines/nchunks
        #elif not nlines is None:
        self.chunksize=nlines
        # else:
        #     raise Exception("ERROR you must specify nlines or nchunks")

        self.keyfn=keyfn

        # the key of the last line
        self.last_key=None

        # index of last line which fh2 will hasn't read,  whose key is different the previous line
        self.last_breakpoint=0  

        # this keeps track of how many lines self.fh is ahead of self.fh2
        self.lines_read=0

        # this is true when self.fh went through the whole file
        self.finished=False

        # on 'next' calls when stuff must returned instead of reading new lines, this is >0
        self.n_to_return=None        
        
    def __iter__(self):    
        return self 

    def __next__(self):
      if not self.n_to_return is None and self.n_to_return>0:
          ##  we already determined we need to return some lines now:          
          self.n_to_return-=1
          return self.fh2.readline()
      
      if self.n_to_return == 0:
          ## this chunk is over
          self.n_to_return=None 
          raise StopIteration  

      if self.finished:
          ## this file is over, if we try to keep iterating we only get stopiterations
          raise StopIteration  

      while True:
          ## time to scan self.fh and determine how many lines to return next
          #  note, at the end we will call recursively self.__next__() so that one element is actually returned
          line=self.fh.readline()
          #print( ' <- read line '+str([line]) )
          if not line:
              self.last_breakpoint=self.lines_read
              self.finished=True
              #print("file is finished")

          else:
              key=self.keyfn(line)
              #print("key = "  + key)
              if key!=self.last_key and not key is None:
                  self.last_breakpoint=self.lines_read
                  #print ('FOUND breakpoint: '+str(self.last_breakpoint) + ' end of ' +str(self.last_key) )
              self.last_key=key

          self.lines_read+=1
          #print("current lines_read = "  + str(self.lines_read)+ " last break = "  + str(self.last_breakpoint))

          if self.finished or (self.lines_read > self.chunksize and self.last_breakpoint>0):
              #print('============ time to return values')
              self.n_to_return=self.last_breakpoint
              self.last_breakpoint=0
              self.lines_read-=self.n_to_return

              # input(f'... self.n_to_return {self.n_to_return}  self.lines_read {self.lines_read}  \n')
              return self.__next__()

    readline=__next__
    
    def read(self, size):
        ### necessary just so pandas accept this as valid IO buffer
        pass
    


def buf_count_newlines_gen(fname):
    """Credit to https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python """
    def _make_gen(reader):
        while True:
            b = reader(2 ** 16)
            if not b: break
            yield b

    with open(fname, "rb") as f:
        count = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
    return count

