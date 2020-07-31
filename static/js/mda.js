let code = (function(){
    return{
      encryptMessage: function(messageToencrypt = '', secretkey = ''){
        var encryptedMessage = CryptoJS.AES.encrypt(messageToencrypt, secretkey);
        return encryptedMessage.toString();
      },
      decryptMessage: function(encryptedMessage = '', secretkey = ''){
        var decryptedBytes = CryptoJS.AES.decrypt(encryptedMessage, secretkey);
        var decryptedMessage = decryptedBytes.toString(CryptoJS.enc.Utf8);

        return decryptedMessage;
      }
    }
})();

function mda_crypt() {
  if (localStorage.getItem("password")) {
      document.getElementById("crypt_textarea").value = code.encryptMessage(document.getElementById("textarea").value, localStorage.getItem("password"))
  }
  else {
      document.getElementById("crypt_textarea").value = code.encryptMessage(document.getElementById("textarea").value, document.getElementById("password").value)
  }
}

function mda_submit() {
  localStorage.clear()
  if (document.getElementById("password").value == '') {
    //document.getElementById("password").value = forge_sha256(document.getElementById("textarea").value);
    localStorage.setItem('password', forge_sha256(document.getElementById("textarea").value));
     // fix "nopassword" after submit form
  }
  else {
    localStorage.setItem('password', document.getElementById("password").value);
  }
  mda_crypt();
}

//console.log(code.encryptMessage('Welcome to AES !','your_password'));
//console.log(code.decryptMessage('U2FsdGVkX1/S5oc9WgsNyZb8TJHsuL7+p4yArjEpOCYgDTUdkVxkmr+E+NdJmro9','your_password'))

//console.log(code.encryptMessage(document.getElementById("textarea").value,document.getElementById("password").value));