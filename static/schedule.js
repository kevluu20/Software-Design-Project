let num = 1;
document.getElementById('add').addEventListener("click",addInput);
function addInput(){
let newInput = '<input type="text" name="input'+num+'"/><br> <br>';
   document.getElementById('others').innerHTML += newInput;  
   num++;
}