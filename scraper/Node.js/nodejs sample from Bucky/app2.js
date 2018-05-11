function placeAnOrder(orderName){
    console.log("Customer order:", orderName)

    cookAndDeliverFood(function () {
        console.log("Deliver food order:",orderName)
    })
}

// Simulate 5 seconds operation
function cookAndDeliverFood(callback){
    setTimeout(callback,5000)
}

// Simulate user web requests
placeAnOrder(1)
placeAnOrder(2)
placeAnOrder(3)
placeAnOrder(4)
placeAnOrder(5)