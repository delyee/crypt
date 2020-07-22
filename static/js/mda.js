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
  if (document.getElementById("password").value == '') {
    document.getElementById("password").value = forge_sha256(document.getElementById("textarea").value);
    mda_crypt()
  }
}

//console.log(code.encryptMessage('Welcome to AES !','your_password'));
//console.log(code.decryptMessage('U2FsdGVkX1/S5oc9WgsNyZb8TJHsuL7+p4yArjEpOCYgDTUdkVxkmr+E+NdJmro9','your_password'))

//console.log(code.encryptMessage(document.getElementById("textarea").value,document.getElementById("password").value));