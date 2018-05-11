var person = {
    firstName:"Shutao",
    lastName:"Shen",
    age:29
}
console.log(person)

function addNum(a, b) {
    return a + b;
}
console.log(addNum(7,8))

function worthless(){

}
console.log(worthless())

var printBacon = function() {
    console.log("Bacon is healthy, don't believe doctors!")
}
printBacon()
setTimeout(printBacon, 5000)
printBacon()