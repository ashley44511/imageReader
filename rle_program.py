#Project 2B

from console_gfx import ConsoleGfx
import copy

def main():
   #displays welcome message, color test, menu, and prompts user for input
   image_data = []
   option = -1
   print("Welcome to the RLE image encoder!\n")
   print("Displaying Spectrum Image: ")
   ConsoleGfx.display_image(ConsoleGfx.test_rainbow)
   print("\n")
   #type all option numbers as strings
   while option != "0":
      #print menu and prompt user to select option
      option = print_menu()
      #call different functions based on user input of option
      if option == "1":
         #loads file input by user and stores file in image_data
         image_data = my_load_file()
      elif option =="2":
         #loads test_image and stores file in image_data
         image_data = my_test_image()
      elif option == "3":
         #reads RLE data from user in hexadecimal notation
         rle_string = input("Enter an RLE string to be decoded: ")
         print() #FIXME ?
         image_data = string_to_rle(rle_string)
         image_data = decode_rle(image_data)
      elif option == "4":
         #reads RLE data from user in hexadecimal notation without delimiters
         rle_string = input("Enter the hex string holding RLE data: ")
         print()
         image_data = decode_rle(string_to_data(rle_string))
      elif option == "5":
         #reads raw data from user in hexadecimal notation
         string = input("Enter the hex string holding flat data: ")
         print() #FIXME ?
         image_data = string_to_data(string)
      elif option == "6":
         #displays image currently stored in image_data
         my_display_image(image_data)
      elif option == "7":
         #converts current data in image_data into human-readable RLE representation w/ delimiters
         print(f"RLE representation: {to_rle_string(encode_rle(image_data))}")
         print() #FIXME ?
      elif option == "8":
         #converts current data in image_data into RLE hexadecimal representation w/out delimeters
         print(f"RLE hex values: {to_hex_string(encode_rle(image_data))}\n")
      elif option == "9":
         #display current raw data in hexadecimal representation
         print(f"Flat hex values: {to_hex_string(image_data)}\n")
   #print("Program Exited.")

def print_menu():
   #prints menu, prompts user for input, and returns selected menu option
   print("RLE Menu\n--------\n0. Exit\n1. Load File\n2. Load Test Image\n3. Read RLE String\n"
   "4. Read RLE Hex String\n5. Read Data Hex String\n6. Display Image\n7. Display RLE String\n"
   "8. Display Hex RLE Data\n9. Display Hex Flat Data\n")
   option = input("Select a Menu Option: ")
   return option

def my_load_file():
   #loads file input by user (string) and returns image data translated by ConsoleGfx.load_file function
   filename = input("Enter name of file to load: ")
   print()
   return ConsoleGfx.load_file(filename)

def my_test_image():
   print("Test image data loaded.\n")
   return ConsoleGfx.test_image

def my_display_image(image_data):
   #uses ConsoleGfx.display_image(image_data) function to output the stored image in image_data variable
   print("Displaying image...")
   ConsoleGfx.display_image(image_data)
   print()

def to_hex_string(data):
   #translates data (RLE or raw) to a hexadecimal string
   hex_string = ""
   #converts data into hexadecimal
   for i in data:
      if (i < 10) and (i > -1):
         hex_string += str(i)
      else:
         if i == 10:
            hex_string += 'a'
         elif i == 11:
            hex_string += 'b'
         elif i == 12:
            hex_string += 'c'
         elif i == 13:
            hex_string += 'd'
         elif i == 14:
            hex_string += 'e'
         elif i == 15:
            hex_string += 'f'
         else:
            print("error")
   return hex_string

def count_runs(flat_data):
   #returns number of runs of data in an image data set; double this result for length of encoded (RLE) list
   num_run = 1
   length = 0
   prev_var = flat_data[0]
   for i in flat_data:
   #adds to length until new value is detected, then resets for next run
   #length is tracked for 15 length limit
      if i == prev_var:
         length += 1
      else:
      #adds to num_run when current value and previous value don't match (new color)
         num_run += 1
         length = 1
      if length > 15:
         num_run += 1
         length = 0
      prev_var = i
   return num_run

def encode_rle(flat_data):
   #returns encoding (in RLE) of the raw data passed in; used to generate RLE representation of data
   flat_data.append(-1) #appends -1 to end so list correctly iterates through all actual data entries
   encoded_list = [] #will hold RLE representation of data
   length = 0
   prev_var = flat_data[0]
   for i in flat_data:
      if i == prev_var:
      #checks for repetitions of a value
         length += 1
      else:
         encoded_list.append(length)
         encoded_list.append(prev_var)
         length = 1
      if length > 14:
      #splits into two runs if run is 15 pixels long
         encoded_list.append(15)
         encoded_list.append(prev_var)
         length = 0
      prev_var = i
   return encoded_list

def get_decoded_length(rle_data):
   #returns decompressed size RLE data; used to generate flat data from RLE encoding
   length = 0
   for i in range(0, len(rle_data)):
      if (i % 2) == 0: #looks at every other entry in rle_data list to find number of times a value is repeated
         length += rle_data[i] #adds repetitions of each value together for total length
   return length

def decode_rle(rle_data):
   #returns the decoded data set from RLE encoded data. This decompresses RLE data for use
   decoded_list = []
   for i in range(0, len(rle_data)):
      if (i % 2) == 0: #looks at every other entry in rle_data list to find number of times a value is repeated
         for j in range(0, rle_data[i]):
         #appends matching value rle_data[i] times to decoded_list
            decoded_list.append(rle_data[i + 1])
   return decoded_list

def string_to_data(data_string):
   #translates a string in hexadecimal format into byte data (can be raw or RLE)
   string_list = [] #holds byte data to be returned
   for i in data_string: #goes through each character in data_string
      #transaltes hexadecimal to decimal for byte data
      if i == 'a' or i == 'A':
         string_list.append(10)
      elif i == 'b' or i == 'B':
         string_list.append(11)
      elif i == 'c' or i == 'C':
         string_list.append(12)
      elif i == 'd' or i == 'D':
         string_list.append(13)
      elif i == 'e' or i == 'E':
         string_list.append(14)
      elif i == 'f' or i == 'F':
         string_list.append(15)
      elif (int(i) < 10) and (int(i) > -1):
         string_list.append(int(i))
      else:
         print("error")
   return string_list

def to_rle_string(rle_data):
   #translates RLE data into a human-readable representation. For each run, in order, it displays run
   #length in decimal (1-2 digits), the run value in hexadecimal (1 digit), and a delimiter ':' between runs
   readable_string = "" #the famous human-readable representation to be returned
   for i in range(0, len(rle_data)):
      if (i % 2) == 0:
         # detects run length and appends decimal value to readable_string
         readable_string += str(rle_data[i])
      else:
         # detects run value and appends hexadecimal value to readable_string
         run_hex_value = to_hex_string([rle_data[i]])
         readable_string += run_hex_value
         if i != (len(rle_data) - 1):
            readable_string += ":"
   return readable_string

def string_to_rle(rle_string):
   #translates a string in human-readable RLE format (with delimiters) into RLE byte data
   pass #FIXME
   # split string with ":" and get last digit of each smaller string
   string_list = rle_string.split(':')
   rle_list = []
   for i in string_list:
      length = i[0:-1]
      run_value = i[-1] #always one digit hex
      run_value = string_to_data(run_value)
      rle_list.extend([int(length), run_value[0]])
   return rle_list




if __name__ == '__main__':
   # calls main function if file run is rle_program.py
   main()

