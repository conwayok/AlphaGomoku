from libc.stdlib cimport malloc, free

cdef int check(int* num_pattern_, int state_c[15][15], int len_num_pattern_):
		cdef int max_needed_matches_to_detect = 2  # for program to run faster
		cdef int num_of_matches = 0
		
		
		# check directions: up, down, left, right, up left, up right, down left, down right
		#cdef int directions[8][2]  # = [[1, 0], [-1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
		cdef int directions[4][2]
		
		#directions[0][:] = [1, 0]
		#directions[1][:] = [-1, 0]
		#directions[2][:] = [0, -1]
		#directions[3][:] = [0, 1]
		#directions[4][:] = [-1, -1]
		#directions[5][:] = [-1, 1]
		#directions[6][:] = [1, -1]
		#directions[7][:] = [1, 1]
		
		directions[0][:] = [1, 0] # |
		directions[1][:] = [0, -1] # --
		directions[2][:] = [-1, 1] # /
		directions[3][:] = [-1, -1] # \
		
		
		cdef int direction_index = 0
		cdef int row = 0
		cdef int col = 0
		cdef int row_index = 0
		cdef int col_index = 0
		cdef int correct = 0
		
		for direction_index in range(4):
			for row in range(15):
				# check if pattern will go out of bounds
				row_index = row + (len_num_pattern_ - 1) * directions[direction_index][0]
				if row_index < 0 or row_index >= 15:
					continue
				for col in range(15):
					col_index = col + (len_num_pattern_ - 1) * directions[direction_index][1]
					if col_index < 0 or col_index >= 15:
						continue

					if state_c[row][col] == num_pattern_[0]:
						correct = 1
						row_index = row + directions[direction_index][0]
						col_index = col + directions[direction_index][1]

						while True:
							if correct == len_num_pattern_:
								#print('correct:', correct)
								#print('found at row', row, 'col', col, 'direction', directions[direction_index][0], directions[direction_index][1])
								num_of_matches += 1
								break

							if state_c[row_index][col_index] != num_pattern_[correct]:
								break

							# correct
							else:
								correct += 1
								row_index += directions[direction_index][0]
								col_index += directions[direction_index][1]

					if num_of_matches >= max_needed_matches_to_detect:
						return num_of_matches
		return num_of_matches

def detect_pattern(list state, str pattern, int player_num):
	cdef int num_of_matches = 0
	cdef player_num_c = player_num
	cdef int state_c[15][15]
	cdef int len_pattern = len(pattern)
	cdef int max_needed_matches_to_detect = 2  # for program to run faster
	
	# indexes
	cdef int i = 0
	cdef int j = 0
	
	for i in range(15):
		for j in range(15):
			state_c[i][j] = state[i][j]
			
	#convert pattern to number list
	cdef int* num_pattern = <int*>malloc(len_pattern * sizeof(int))
	# cdef int pattern_index
	for pattern_index in range(len(pattern)):
		#print(pattern[pattern_index])
		if pattern[pattern_index] == '-':
			num_pattern[pattern_index] = 0
		elif pattern[pattern_index] == 'o':
			num_pattern[pattern_index] = player_num
	
	num_of_matches = check(num_pattern, state_c, len_pattern)
	if num_of_matches >= max_needed_matches_to_detect:
		free(num_pattern)
		return num_of_matches
	
	i = 0
	# also check flipped pattern if needed
	cdef int* flipped_pattern = <int*>malloc(len_pattern * sizeof(int))
	for i in range(len_pattern):
		flipped_pattern[i] = num_pattern[len_pattern - i - 1]
	
	i = 0
	for i in range(len_pattern):
		if num_pattern[i] != flipped_pattern[i]:
			#print('checking flipped pattern')
			num_of_matches += check(flipped_pattern, state_c, len_pattern)
			free(num_pattern)
			break
	
	return num_of_matches
