var Bucky = {
    printFirstName : function () {
        console.log("My name is Bucky")
        console.log(this === Bucky)
    }
}
Bucky.printFirstName()

// the default calling object is global
function doSomethingWorthless(){
    console.log("\nI'm worthless")
    console.log(this === global)
}

doSomethingWorthless()