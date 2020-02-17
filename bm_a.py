from page import page
from frame import frame
from dm import diskManager

class BufferPoolFullError(Exception):
	#exception used in the Clock class
	def __init__(self, message):
		self.message = message

class clock:
	def __init__(self):
		# do the required initializations
		self.frameNumber = 0
		self.errMessage = BufferPoolFullError("Error. BufferPoolFull\n")
		#self.pinCount 	 = 1
		#self.dirtyBit 	 = False
		#self.referenced  = 1
		#self.pageNumber	 = 0

		#expression if condition else expression2
	def pickVictim(self,buffer):
	# find a victim page using the clock algorithm and return the frame number
	# if all pages in the buffer pool are pinned, raise the exception BufferPoolFullError
		for i in range(len(buffer)): 
			if buffer[i].referenced > 0: 
				buffer[i].referenced -= 1

		for i in range(len(buffer)):
			if buffer[i].pinCount == 0 and buffer[i].referenced == 0:
    				return i
			elif not buffer[i].pinCount == 0 and not buffer[i].referenced == 0:
    				print(self.errMessage)
		return 0

					
#==================================================================================================
		
class bufferManager:
	
	def __init__(self,size):
		self.buffer = []
		self.clk = clock()
		self.dm = diskManager()
		for i in range(size):
			self.buffer.append(frame()) # creating buffer frames (i.e., allocating memory)
			self.buffer[i].frameNumber = i
		
	#------------------------------------------------------------

	def pin(self,pageNumber, new = False): 
		# given a page number, pin the page in the buffer
		# if new = True, the page is new so no need to read it from disk
		# if new = False, the page already exists. So read it from disk 
		#if it is not already in the pool. 
		i = pageNumber%(len(self.buffer))
		self.buffer[i].currentPage.pageNo = pageNumber
		self.buffer[i].currentPage.content = "content {}".format(pageNumber)
		self.buffer[i].pinCount = 1
		self.buffer[i].referenced = 1
		self.buffer[i].dirtyBit = False
		return pageNumber
		
	
	#------------------------------------------------------------
	def unpin(self,pageNumber, dirty):
		i = pageNumber%len(self.buffer)
		if(i >= len(self.buffer)):
			victim = self.clk.pickVictim(self.buffer)
			self.buffer[victim].dirtyBit = True
			self.buffer[victim].pinCount = 0
			self.buffer[victim].referenced = 0
			self.flushPage(victim)
			return victim	
		self.buffer[i].dirtyBit = True
		self.buffer[i].pinCount = 0
		self.buffer[i].referenced = 0
		return i

	def pageNumber(self, pageNumber):
    		i = pageNumber%len(self.buffer)
    		return self.buffer[i].currentPage.pageNo

	def pageContent(self, pageNumber):
    		i = pageNumber%len(self.buffer)
    		return self.buffer[i].currentPage.content
	
			
		

	def flushPage(self,pageNumber): 
		# Ignore this function, it is not needed for this homework.
		# flushPage forces a page in the buffer pool to be written to disk
		for i in range(len(self.buffer)):
			if self.buffer[i].currentPage.pageNo == pageNumber:
				self.dm.writePageToDisk(self.buffer[i].currentPage) # flush writes a page to disk 
				self.buffer[i].dirtyBit = False

	def printBufferContent(self): # helper function to display buffer content on the screen (helpful for debugging)
		print("---------------------------------------------------")
		for i in range(len(self.buffer)):
			print("frame#={} pinCount={} dirtyBit={} referenced={} pageNo={} pageContent={} ".format(self.buffer[i].frameNumber, self.buffer[i].pinCount, self.buffer[i].dirtyBit, self.buffer[i].referenced,  self.buffer[i].currentPage.pageNo, self.buffer[i].currentPage.content))	
		print("---------------------------------------------------")
