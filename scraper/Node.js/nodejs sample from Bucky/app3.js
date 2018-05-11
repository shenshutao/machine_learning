var Bucky = {
    favFood: "Bacon",
    favMovie: "Chappie"
}

var Person = Bucky
Person.favFood = "Hot dog"
console.log(Bucky.favFood)


console.log(19 == '19') //true   value only
console.log(19 === '19') //false  value & type