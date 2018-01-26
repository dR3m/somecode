from PIL import Image
class LSB:
    img = Image.Image()
    data = []
    bpixl = []
    msg = ''
    chanels = {'r':0, 'g': 1, 'b':2 }
    
    def __init__(self,path):
        self.img = Image.open(path) 
        self.data = self.img.getdata()
        self.analyse('analyse_original')
        print('wait...')
               
    def analyse(self, name):
#        self.bpixl = [list(map(lambda x:'{:0>8}'.format(bin(x)[2:]), rgb)) for rgb in self.data] 
        self.bpixl = [list(map(lambda x: format(x, '08b'), rgb)) for rgb in self.data]                  
        f = [list(map(lambda x: '1'*8 if x[-1]=='1' else '0'*8, rgb)) for rgb in self.bpixl]
        pxls = [tuple(map(lambda x: int(x,2),b)) for b in f]
        new_img = Image.new("RGB", (self.img.size[0], self.img.size[1]), "black")
        new_img.putdata(pxls)
        new_img.save(name + '.png')
        
        
    def decode(self, c):
        if c == 'a':
            tmp = ''.join([''.join(list(map(lambda x:bin(x)[-1],px))) for px in self.data])                      
        else: 
            tmp = ''.join([bin(px[self.chanels[c]])[-1] for px in self.data])
        for n in range(0,len(tmp),8):
            if  int(tmp[n:n+8],2) in range(32,127):
                self.msg += chr(int(tmp[n:n+8],2))
            else:
                break
        return self.msg  
        
    
    def encode(self, _msg, _c):
        bits_of_msg = ''.join([format(ord(l), '08b') for l in _msg])
        new_data = []
        if _c == 'a':
                for px in self.bpixl:
                    if bits_of_msg != '' and len(bits_of_msg)>2:
                        new_data.append(tuple(int(px[c][:-1]+bits_of_msg[c],2) for c in range(3)))
                        bits_of_msg = bits_of_msg[3:] 
        else:
                for px in self.bpixl:
                    if bits_of_msg != '':
                        new_data.append(tuple(int(px[c][:-1]+bits_of_msg[0],2) if self.chanels[_c] == c else int(px[c],2) for c in range(3)))
                        bits_of_msg = bits_of_msg[1:]
                    else: 
                        new_data.append(tuple(int(i,2) for i in px))
        self.img.putdata(new_data)
        self.img.save('encoded.png', 'PNG')
#        LSB.analyse(self, 'analyse_2')
        

def main():
#   path = input('Input path: ')
#   img = LSB(path)
    img = LSB('/home/drem/Documents/sharevm/squareCTF/stegasaurus.png') 
    r = img.decode('r')
    g = img.decode('g')
    b = img.decode('b')
    a = img.decode('a')
    print(r,g,b,a)
     
if __name__ == '__main__':
    main()            
