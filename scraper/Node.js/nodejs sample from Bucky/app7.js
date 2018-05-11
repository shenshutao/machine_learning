function User() {
    this.name = ""
    this.life = 100;
    this.giveLife = function (targetPlayer) {
         targetPlayer.life += 1;
         console.log(this.name, "give 1 life to", targetPlayer.name)
    }
}

var bucky = new User();
var wendy = new User();
bucky.name = "Bucky"
wendy.name = "Wendy"

bucky.giveLife(wendy)
console.log("Bucky:", bucky.life)
console.log("Wendy:", wendy.life)

User.prototype.upperCut = function (targetPlayer) {
    targetPlayer.life -= 3;
    console.log(this.name, "just uppercutted", targetPlayer.name)
}

wendy.upperCut(bucky)
console.log("Bucky:", bucky.life)
console.log("Wendy:", wendy.life)

User.prototype.magic = 60;
console.log(bucky.magic)
console.log(wendy.magic)