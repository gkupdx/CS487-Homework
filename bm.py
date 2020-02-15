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
		self.referenced = 1
		self.errorMessage = ''
		#pass

	def pickVictim(self, buffer):
		# find a victim page using the clock algorithm and return the frame number
		# if all pages in the buffer pool are pinned, raise the exception BufferPoolFullError

		# Initialize the frameNumber for each frame in buffer pool
		# Confirmed by Hisham that it was okay to do this here
		for i in range(len(buffer)):
			buffer[i].frameNumber = i

		victimFrameNum = -1
		found = False

		while found is False:
			for i in range(len(buffer)):
				if buffer[i].pinCount == 0: #pinCount is 0 so possible candidate
					if buffer[i].referenced == 1: #flip reference bit, give it a 2nd chance
						buffer[i].referenced = 0
					else: #referenced is 0 so very likely to be candidate
						if buffer[i].dirtyBit == True: #but page needs to be written to disk
							self.dm.writePageToDisk(buffer[i].currentPage)
							victimFrameNum = buffer[i].frameNumber
							found = True
							break
						else: #no need to write to disk, just evict
							victimFrameNum = buffer[i].frameNumber
							found = True
							break

		if victimFrameNum == -1:
			self.errorMessage = BufferPoolFullError("All pages in buffer pool are pinned!")

		return victimFrameNum
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

	def pin(self,pageNumber, new):
		# given a page number, pin the page in the buffer
		# if new = True, the page is new so no need to read it from disk
		# if new = False, the page already exists. So read it from disk if it is not already in the pool.
		#for i in range(len(self.buffer)):
		#	if self.buffer[i].currentPage.pageNo == pageNumber: #we have a matching page in our pool
		#		self.buffer[i].pinCount += 1
		#	else: #page is new so need to read in from disk
		#		self.dm.readPageFromDisk(self.buffer[i].currentPage)
		pass
    
	#------------------------------------------------------------
	def unpin(self, pageNumber, dirty):
		for i in range(len(self.buffer)):
			if self.buffer[i].currentPage.pageNo == pageNumber:
				self.buffer[i].currentPage.pinCount -= 1
				if dirty is True:
					self.buffer[i].currentPage.dirtyBit = True
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
