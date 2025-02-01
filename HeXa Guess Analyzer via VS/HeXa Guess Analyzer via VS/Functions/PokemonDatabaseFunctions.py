
from PIL import Image

"""
def ScanForPokemonInDatabase(update, context):
"""

def scanRGB(picture):
    
    imgobj = Image.open(picture)
    pixels = imgobj.convert('RGBA')
    data = pixels.getdata()
    lofpixels = []
    for pixel in data:
        lofpixels.extend(pixel)
        
    #CAN BE TWEAKED
    lofpixels = sum(lofpixels)
    #--
        
    return lofpixels

def AddToTxtDatabase(RGBList, name):
    
    try:
        isExist, match = ScanTxtDatabaseForMatches(RGBList)
        if not isExist:
            with open("Databases\Pokemons Database.txt", "a") as fileObject:
                fileObject.write(str(RGBList) + "###" + name + "\n")
                print("Data successfully stored.")
                fileObject.close()
                return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
        
def ScanTxtDatabaseForMatches(RGBList = None, onlyCount = False, onlyExamples = False):
    
    counter = 0
    examples = list()

    try:
        with open("Databases\Pokemons Database.txt") as fileObject:
            for eachline in fileObject:
                if onlyCount:
                    counter += 1
                    continue
                elif onlyExamples:
                    if counter > 10:
                        break
                    else:
                        counter += 1
                        examples.append(eachline)
                        continue
                elif not eachline.startswith(str(RGBList)):
                    continue
                splitLine = eachline.split("###")
                print("Record found.")
                return True, splitLine[1]
            if onlyCount:
                return True, counter
            elif onlyExamples:
                return True, examples
            else:
                return False, None
    except Exception as e:
        print(e)
        return False, None

def SortDatabaseByNumber():

    temp_list = list()
    try:
        with open("Databases\Pokemons Database.txt") as fileObject:
            for eachline in fileObject:
                temp_list.append(eachline)
            fileObject.close()

        temp_list.sort()

        with open("Databases\Pokemons Database.txt", "w") as fileObject:
            for item in temp_list:
                fileObject.write(item)
            fileObject.close()
            return True

    except Exception as e:
        print(e)
        return False

def GetPokemonsListFromDatabase():

    try:
        with open("Databases\Pokemons Database.txt") as fileObject:
            temp_list = fileObject.readlines()
            fileObject.close()

        return True, temp_list

    except Exception as e:
        print(e)
        return False, None

def GetPokemonByIndex(the_list, index):

    try:
        x = the_list[index][13:]
        return True, x

    except Exception as e:
        print(e)
        return False, None