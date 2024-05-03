import tempfile
import os
from flask import Flask, request, redirect, send_file, render_template
from skimage import io
from skimage.transform import resize
import base64
import glob
import numpy as np

app = Flask(__name__)

main_html = """
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="static/styles.css">
	</head>
	<script>
	  var mousePressed = false;
	  var lastX, lastY;
	  var ctx;

	   function getRndInteger(min, max) {
	    return Math.floor(Math.random() * (max - min) ) + min;
	   }

	  function InitThis() {
	      ctx = document.getElementById('myCanvas').getContext("2d");


	      numero = getRndInteger(0, 10);
	      letra = ["Niebla","Roca","Hojas","Arena","Nubes"];
	      random = Math.floor(Math.random() * letra.length);
	      aleatorio = letra[random];

	      document.getElementById('mensaje').innerHTML  = 'Escribe el simbolo de la aldea escondida entre ' + aleatorio;
	      document.getElementById('numero').value = aleatorio;

	      $('#myCanvas').mousedown(function (e) {
		  mousePressed = true;
		  Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
	      });

	      $('#myCanvas').mousemove(function (e) {
		  if (mousePressed) {
		      Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
		  }
	      });

	      $('#myCanvas').mouseup(function (e) {
		  mousePressed = false;
	      });
	  	    $('#myCanvas').mouseleave(function (e) {
		  mousePressed = false;
	      });
	  }

	  function Draw(x, y, isDown) {
	      if (isDown) {
		  ctx.beginPath();
		  ctx.strokeStyle = 'black';
		  ctx.lineWidth = 11;
		  ctx.lineJoin = "round";
		  ctx.moveTo(lastX, lastY);
		  ctx.lineTo(x, y);
		  ctx.closePath();
		  ctx.stroke();
	      }
	      lastX = x; lastY = y;
	  }

	  function clearArea() {
	      ctx.setTransform(1, 0, 0, 1, 0, 0);
	      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
	  }

	  //https://www.askingbox.com/tutorial/send-html5-canvas-as-image-to-server
	  function prepareImg() {
	     var canvas = document.getElementById('myCanvas');
	     document.getElementById('myImage').value = canvas.toDataURL();
	  }



	</script>
	
	<body onload="InitThis();">
	    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
	    <script type="text/javascript" ></script>
	    <div align="center">
		<h1 id="mensaje">Dibujando...</h1>
		<canvas id="myCanvas" width="200" height="200" style="border:2px solid black"></canvas>
		<br/>
		<br/>
		<div id="botones1">
		      <button onclick="javascript:clearArea();return false;">Borrar</button>
		      <form method="post" action="upload" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="Enviar">
		      </form>
	    	</div>
	    	
		<div id="botones2">
			<form method="get" action="prepare" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="prepara datos">
		      </form>
		      <form method="get" action="Niebla.npy" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="descargar Niebla">
		      </form>
		      <form method="get" action="Roca.npy" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="decargar Roca">
		      </form>
		      <form method="get" action="Hojas.npy" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="decargar Hojas">
		      </form>
		      <form method="get" action="Arena.npy" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="decargar Arena">
		      </form>
		      <form method="get" action="Nubes.npy" onsubmit="javascript:prepareImg();"  enctype="multipart/form-data">
			      <input id="numero" name="numero" type="hidden" value="">
			      <input id="myImage" name="myImage" type="hidden" value="">
			      <input id="bt_upload" type="submit" value="decargar Nubes">
		      </form>
		</div>
		
		
		
	    </div>
	    
	    <div id="imagen" align="center">
      		<img src="https://www.shutterstock.com/image-vector/bandung-indonesia-december-6-2023-600w-2397323497.jpg" width="300"/>
    	    </div>
	</body>
</html>

""" 
@app.route("/")
def main():
    render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        img_data = request.form.get('myImage').replace("data:image/png;base64,", "")
        aleatorio = request.form.get('numero')
        folder_id = '1bjhGYXx9opwIgZj4FO95we5TpBep92S7'  # Reemplaza con la ID de tu carpeta en Google Drive
        file_name = aleatorio + '_image.png'
        with tempfile.NamedTemporaryFile(delete = False, mode = "w+b", suffix='.png', dir=str(aleatorio)) as fh:
            fh.write(base64.b64decode(img_data))
        print(f"Image uploaded {file_name}")
    except Exception as err:
        print("Error occurred")
        print(err)

    return redirect("/", code=302)
    
@app.route('/prepare', methods=['GET'])
def prepare_dataset():
    d = ["Niebla","Roca","Hojas","Arena","Nubes"]
    for digit in d:
        images = []
        filelist = glob.glob('{}/*.png'.format(digit))
        images_read = io.concatenate_images(io.imread_collection(filelist))
        images_read = images_read[:, :, :, 3]
        images.append(images_read)
        images = np.vstack(images)
        np.save('{}.npy'.format(digit), images)
    return "Data set procesado exitosamente"

@app.route('/Niebla.npy', methods=['GET'])
def download_Niebla():
    return send_file('./Niebla.npy')

@app.route('/Roca.npy', methods=['GET'])
def download_Roca():
    return send_file('./Roca.npy')

@app.route('/Hojas.npy', methods=['GET'])
def download_Hojas():
    return send_file('./Hojas.npy')

@app.route('/Arena.npy', methods=['GET'])
def download_Arena():
    return send_file('./Arena.npy')

@app.route('/Nubes.npy', methods=['GET'])
def download_Nubes():
    return send_file('./Nubes.npy')
    
if __name__ == "__main__":
    
    digits = ["Niebla","Roca","Hojas","Arena","Nubes"]
    for d in digits:
        if not os.path.exists(str(d)):
            os.mkdir(str(d))
    app.run()
