import base64
import requests
import json
import os



class CRAFileUploader :

  def GetURI(self) :
    if self.ownerComp.par.Usedev == True :
      return "http://localhost:3090/api/stamp"
    else :
      return "https://et-general-services-d8c893e4fb2f.herokuapp.com/api/stamp"

  def __init__(self, ownerComp) :
    self.ownerComp = ownerComp
    self._uri= "http://localhost:3090/api/stamp"
   # self._uri = "https://cramer-file-service-prod.herokuapp.com/api/stamp"

    

  def UploadFiles(self,final_fp) :
    print("sending request  ")
    with open(final_fp, 'rb') as final_file:
      payload = [
        ('file', final_file)
      ]
      data = {
        'alt_uri' : self.ownerComp.par.Site.eval()
      }
      headers = {}
      resp= requests.request("POST", self.GetURI(), data=data,headers=headers, files=payload)

      print("response received")
      print(resp.status_code)
      print(resp.text)

      data = json.loads(resp.text)
      if(resp.status_code == 200) :
        s_data = data["code"].split(',')[1]
        img_bytes = base64.b64decode(s_data)
        ba = bytearray(img_bytes)
        file_name = os.path.basename(os.path.splitext(final_fp)[0])
        vfs_addr = f'{file_name}_code.png'

        # overwrite the vfs if it exists
        if  len(self.ownerComp.vfs.find(pattern=vfs_addr)) > 0:
          self.ownerComp.vfs[vfs_addr].destroy()

        self.ownerComp.vfs.addByteArray(ba,vfs_addr)
        self.ownerComp.op('movie_in').par.file.expr = f"""me.parent().vfs['{vfs_addr}']"""



        # if we are overwritting the files we need to pulse the reload on the parameter to update the movieplay
        self.ownerComp.op('movie_in').par.reloadpulse.pulse()





    # convert to a byte array



    pass
    


