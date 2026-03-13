let currentPage = "on"

function slideTo(id){

if(id === currentPage) return

const curr = document.getElementById(currentPage)
const next = document.getElementById(id)

/* limpiar estados */

curr.classList.remove("active")
curr.classList.add("prev")

next.classList.remove("prev")
next.classList.add("active")

/* limpiar animación anterior */

setTimeout(()=>{
curr.classList.remove("prev")
},400)

currentPage = id

setActiveButton(id)

}

function setActiveButton(id){

document.querySelectorAll(".nav-card").forEach(b=>{
b.classList.remove("active")
})

const map = {
on:0,
off:1,
res:2
}

document.querySelectorAll(".nav-card")[map[id]].classList.add("active")

}

function toggleSidebar(){

const sidebar = document.getElementById("sidebar")
const toggle = document.getElementById("toggle")

sidebar.classList.toggle("hidden")

/* fuerza reflow para que la animación de páginas no se rompa */

document.querySelector(".stack").style.width =
sidebar.classList.contains("hidden") ? "100%" : ""

toggle.innerHTML =
sidebar.classList.contains("hidden") ? "❯" : "❮"

}