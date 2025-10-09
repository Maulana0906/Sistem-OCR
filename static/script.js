const video = document.getElementById('video');
let stream = null;
const canvas = document.getElementById('canvas')
const scc = document.getElementById('scc')
const audio = document.getElementById('audio')

async function startVideo(){
    try{
        const constraints = { video: {
                width: { ideal: 1280 },
                height: { ideal: 720 }},
                audio: false};
        stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;

    }catch(err){
        console.log(err)
    }
}
    startVideo();

setInterval(async () => {
    const videoRect = video.getBoundingClientRect();
    const areaRect = scc.getBoundingClientRect()
    const scaleX = video.videoWidth / videoRect.width;
    const scaleY = video.videoHeight / videoRect.height;

    const sx = (areaRect.left - videoRect.left) * scaleX;
    const sy = (areaRect.top - videoRect.top) * scaleY;
    const sWidth = areaRect.width * scaleX;
    const sHeight = areaRect.height * scaleY;

    canvas.width = sWidth;
    canvas.height = sHeight;

    const context = canvas.getContext('2d');
    context.drawImage(video, sx, sy, sWidth, sHeight, 0, 0, scc.clientWidth , scc.clientHeight);
    const dataURL = canvas.toDataURL('image/png')

  try {
    const res = await fetch('http://127.0.0.1:5000/ocr', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: dataURL })
    });

    const data = await res.blob();
    const url = URL.createObjectURL(data)
    const audio = new Audio(url);
    audio.play()

  } catch (error) {
    console.log('Error:', error);
  }


},4000)


//sudah install tesseract nya