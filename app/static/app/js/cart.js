var updateBtns = document.getElementsByClassName('update-cart')

for ( i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId, action)
    })
}

function updateUserOrder(productId, action){
    var url = '/update_item/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
        },
        body: JSON.stringify({'productId': productId,'action': action})
    })
    .then((respone) =>{
        return respone.json()
    })
    .then((data) =>{
        console.log('data', data)
    })
}