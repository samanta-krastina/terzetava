let zina = document.getElementById('zina');
let zinas = document.querySelector('.logs');
async function IELADET_ZINAS(){
  let datiNoServera = await fetch('/read_msg');
  let dati = await datiNoServera.json();
  let teksts = "";
  for(let i = 0; i < await dati.length; i++)
      teksts = teksts+ "[" + dati[i].laiks + "] <b>" + dati[i].vards + ":</b> " +  dati[i].zina + "<br />";
  zinas.innerHTML = teksts;
  zinas.scrollTop = zinas.scrollHeight;
}
setInterval(IELADET_ZINAS, 1000);

function NOSUTIT_ZINU(){
  let vards = document.getElementById('vards');
  if(vards.value != ""){
    if(zina.value != ""){
      fetch('/sutit/'+vards.value+'/'+zina.value);
      zina.value = "";
    }else{
      alert("Ieraksti ziņu!");
    }
  }else{
    alert("Tērzētava nepieļauj anonīmu ziņu iesniegšanu!");
  }
}