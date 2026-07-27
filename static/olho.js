const senhaInput = document.getElementById("senha");
const mostrarSenha = document.getElementById("mostrarsenha");
const erroSenha = document.getElementById("errosenha");
const btnCadastro = document.getElementById("btncadastro");

mostrarSenha.addEventListener("click", () => {
    if (senhaInput.type === "password"){
        senhaInput.type = "text";
        mostrarSenha.classList.replace("fa-eye-slash", "fa-eye");
    } else {
        senhaInput.type = "password";
        mostrarSenha.classList.replace("fa-eye", "fa-eye-slash");
    }
});

//validação de senha

const regexSenha = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%¨&*()_+\-=\[\]{};':"\\|,.<>\/?]).{8,}$/;

senhaInput.addEventListener("input", () =>{
    const senha = senhaInput.value;

    if(!regexSenha.test(senha)){
        erroSenha.textContent = "A senha não cumpre os requisitos";
        senhaInput.style.border = "2px solid red";
        btnCadastro.disable = true;
    } else {
        erroSenha.textContent = "";
        senhaInput.style.border = "2px solid #7b2cff";
        btnCadastro.disable = false;
        }
});

//Bloqueia a senha caso não cumpra os requisitos

btnCadastro.addEventListener("click", (e) =>{
    if (!regexSenha.test(senhaInput.value)) {
        e.preventDefault();
        alert("Senha inválida! Corrija antes de se cadastrar");
    }
});