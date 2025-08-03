

function showAlert(name) {
  alert("Bạn vừa chọn sản phẩm:" + name);
}


const chatbot=document.querySelector("#chatbot")
document.getElementById('product-form').addEventListener('submit',function(e){
  e.preventDefault
  var form=e.target
  var formData=new FormData(form)
  fetch('api/products/create',{
    method:'POST',
    headers:{
      'X-CSRFToken':'{{csrf_token}}',
    },
    body:formData,
  })
  .then(response=>response.json())
  .then(data=>{alert('Them thanh cong san pham')})
  .catch(error=>{
    console.error('Error:',error);
    alert("Xay ra loi khi them san pham");
  })
})