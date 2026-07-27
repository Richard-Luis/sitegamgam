const senhaInput = document.getElementById("senha");
const mostrarSenha = document.getElementById("mostrarsenha");
const erroSenha = document.getElementById("errosenha");
const btnCadastro = document.getElementById("btncadastro");
const senhaRegras =  document.getElementById("regras-senha");

mostrarSenha.addEventListener("click", () => {
    if (senhaInput.type === "password"){
        senhaInput.type = "text";
        mostrarSenha.classList.replace("fa-eye-slash", "fa-eye");
    } else {
        senhaInput.type = "password";
        mostrarSenha.classList.replace("fa-eye", "fa-eye-slash");
    }
});

const regexSenha = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%¨&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;

btnCadastro.addEventListener("click", (e) =>{
    const senha = senhaInput.value;

    if(!regexSenha.test(senha)){
        e.preventDefault();
        erroSenha.textContent = "A senha não cumpre os requisitos";
        senhaInput.style.border = "2px solid red";
    } else {
        erroSenha.textContent = "";
        senhaInput.style.border = "2px solid #7b2cff";
        }
});

btnCadastro.addEventListener("click", (e) =>{
    if (!regexSenha.test(senhaInput.value)) {
        e.preventDefault();
        alert("Senha inválida! Corrija antes de se cadastrar");
    }
});

senhaInput.addEventListener("input", () =>{
    const senha = senhaInput.value;

    const regras = {
        minimo: senha.length >= 8,
        maiuscula: /[A-Z]/.test(senha),
        numero: /[0-9]/.test(senha),
        especial: /[!@#$%¨&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(senha)
    }

    for(const regra in regras){
        const item = document.getElementById(regra);
        if(regras[regra]){
            item.style.color = "green"
        } else {
            item.style.color = "red"
        }
    }
})