function val() {
  
    var curs = document.getElementById("select_id").value;
    var stu = document.getElementById("STU_ID").value;
     
    if (stu != "" && stu.length == 9){
    const data = JSON.stringify({
        'cours': curs,
        'STU_': stu
      })
      
      const xhr = new XMLHttpRequest()
      xhr.withCredentials = true;
      
      xhr.addEventListener('readystatechange', function() {
        if (this.readyState === this.DONE) {
          console.log(this.responseText)

          alert(this.responseText);
        }
      });
      
      xhr.open('POST', '/attend') ;
      xhr.setRequestHeader('content-type', 'application/json')
      xhr.send(data);
    
    
    }else{
        alert("Code must be filled out");
    return false;
    }
    
 
 }


 function Quize() {
  
  var curs = document.getElementById("course").value;
  var stu = document.getElementById("ID").value;
  var mark = document.getElementById("myRange").value;
   
  if (stu != "" && stu.length == 9){
  const data = JSON.stringify({
      'cours': curs,
      'STU_': stu,
      'Mark':mark
      
    })
    
    const xhr = new XMLHttpRequest()
    xhr.withCredentials = true;
    
    xhr.addEventListener('readystatechange', function() {
      if (this.readyState === this.DONE) {
        console.log(this.responseText)

        alert(this.responseText);
      }
    });
    
    xhr.open('POST', '/Quizdata') ;
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.send(data);
  
  
  }else{
      alert("Code must be filled out");
  return false;
  }
  

}


function ViewQuize() {
  var curs = document.getElementById("courseV").value;
  var stu = document.getElementById("Week").value;
  
  
  const data = JSON.stringify({
      'cours': curs,
      'Week': stu,
     
      
    })
    
    const xhr = new XMLHttpRequest()
    xhr.withCredentials = true;
    
    xhr.addEventListener('readystatechange', function() {
      if (this.readyState === this.DONE) {
        console.log(this.responseText)

        alert(this.responseText);
      }
    });
    
    xhr.open('POST', '/Quizdata/view') ;
    xhr.setRequestHeader('content-type', 'application/json')
    xhr.send(data);
  
  
 

  

}




