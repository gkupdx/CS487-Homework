from page import page
from frame import frame
from dm import diskManager

class BufferPoolFullError(Exception):
	#exception used in the Clock class
	def __init__(self, message):
		self.message = message

class clock:
	def __init__(self):
		self.frameNumber = 0
		self.errorMessage = BufferPoolFullError("Buffer pool is full!\n")
		#pass

	def pickVictim(self, buffer):
		# find a victim page using the clock algorithm and return the frame number
		# if all pages in the buffer pool are pinned, raise the exception BufferPoolFullError

		# Initialize the frameNumber for each frame in buffer pool
		# Confirmed by Hisham that it was okay to do this here
		for i in range(len(buffer)):
			buffer[i].frameNumber = i

		for i in range(len(buffer)):
			if buffer[i].referenced > 0:
				buffer[i].referenced -= 1

		for i in range(len(buffer)):
			if buffer[i].pinCount == 0 and buffer[i].referenced == 0:
				return i

		print(self.errorMessage)

		return -1
		#pass
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

	def pin(self, pageNumber, new):
		# given a page number, pin the page in the buffer
		# if new = True, the page (we created) is new so can't read it from disk but it might be in the pool
		# if new = False, the page already exists. So read it from disk if it is not already in the pool.
		if new is True:
			for i in range(len(self.buffer)): #check if page is in pool
				if self.buffer[i].currentPage.pageNo == pageNumber:
					self.buffer[i].pinCount += 1
					return self.buffer[i].currentPage

			#page is not in pool so we have to evict a page
			clk = clock()
			victimPage = clk.pickVictim(self.buffer)
			for i in range(len(self.buffer)):
				if self.buffer[i].frameNumber == victimPage: #this is the frame number with page we want to evict
					self.unpin(pageNumber, self.buffer[i].dirtyBit) #run unpin function
					self.buffer[i].currentPage.pageNo = pageNumber # "create" the new page and return this page
					self.buffer[i].pinCount = 1
					self.buffer[i].referenced = 1
					self.buffer[i].dirtyBit = False
					return self.buffer[i].currentPage


		else: #new = False, page already exists
			for j in range(len(self.buffer)): #check if page is already in pool
				if self.buffer[j].currentPage.pageNo == pageNumber:
					self.buffer[j].pinCount += 1
					return self.buffer[j].currentPage
			return self.dm.readPageFromDisk(pageNumber)

		pass
    
	#------------------------------------------------------------
	def unpin(self, pageNumber, dirty):
		for i in range(len(self.buffer)):
			if self.buffer[i].currentPage.pageNo == pageNumber:
				self.buffer[i].pinCount -= 1
				if dirty is True and self.buffer[i].pinCount == 0: #completely remove from buffer pool and write to disk
					self.dm.writePageToDisk(self.buffer[i].currentPage)

		pass

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
