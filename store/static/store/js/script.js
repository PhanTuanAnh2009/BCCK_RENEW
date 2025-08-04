

// document.addEventListener('DOMContentLoaded',function(){


// })

document.getElementById('product-form').addEventListener('submit',function(e){
  e.preventDefault()
  var form=e.target
  var formData=new FormData(form)
  fetch('/api/products/create',{
    method:'POST',
    headers:{
      'X-CSRFToken':'{{csrf_token}}',
    },
    body:formData,
  })
  .then(response=>response.json())
  .then(()=>window.location.href='/products/')
})
