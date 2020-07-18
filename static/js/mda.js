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
  document.getElementById("crypt_textarea").value = code.encryptMessage(document.getElementById("textarea").value,document.getElementById("password").value)
}

function mda_hash() {
  document.getElementById("password").value = forge_sha256(document.getElementById("password").value)
}

//console.log(code.encryptMessage('Welcome to AES !','your_password'));
//console.log(code.decryptMessage('U2FsdGVkX1/S5oc9WgsNyZb8TJHsuL7+p4yArjEpOCYgDTUdkVxkmr+E+NdJmro9','your_password'))

//console.log(code.encryptMessage(document.getElementById("textarea").value,document.getElementById("password").value));