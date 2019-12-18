import React, { useState, useEffect } from 'react';
import useForm from "react-hook-form";
import './App.css';

function App() {
  const { handleSubmit, register, errors } = useForm({});
  const [hasError, setErrors] = useState(false);
  const [pictures, setPictures] = useState([]);
  
  async function fetchData(count) {
    await fetch("http://127.0.0.1:5000/" + count, {
      headers: {
        'Cache-Control': 'no-cache'
      }
    }).then(
      function(response){
        console.log(count)
        response
          .blob()
          .then(res => {
            console.log(res);
            // console.log("data:image/jpeg;base64," + hexToBase64(res));  
            // var hej = new Blob([res], {type: "image/jpeg"})
            let fileReader = new FileReader();
            fileReader.readAsDataURL(res); 
            fileReader.onload = () => { 
              let result = fileReader.result; 
              console.log(result); 
              setPictures(oldArray => [...oldArray, {result, count}]);
            }; 
            // setPictures('data:image/jpeg;base64,' + hexToBase64(res));
            }
            )
          .catch(err => {
            setErrors(err)});
          }
    )
    // var ds = await res.json();
    // console.log(ds);
    
  }

  // var demoPictures = {"Pictures": ["/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png"]}
  
    useEffect(() =>
    {
      for(var i = 0 ; i < 9; i++){
        fetchData(i)
      }
    }
  , []);
  
  //setPictures({"Pictures": som})

  const onSubmit = values => {
    console.log(values)
    fetch('http://127.0.0.1:5000/', {
			method: 'POST',
			body: JSON.stringify(values),
			headers: {
				"Content-type": "application/json; charset=UTF-8"
			}
		}).then(response => {
        window.location.reload()
				return response.json()
			}).then(json => {
				this.setState({
					user:json
				});
			});
  };

  return (
    <div>
      <header>
        <h1>Do pictures contain fish or not</h1>
      </header>
      <div className="row">
      <div className="col-sm-2">
      </div>
      <div className="col-sm-8">
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="flex-container">
            {pictures.map(function(stuff, index){
              return (
                <div key={index} className='flex-item'>
                  <img className="picture" src={stuff.result} aria-hidden='' alt='' /><br/>
                  <input name={"Pictures[" + index + "].count"} ref={register({validate: value => value.String})} value={stuff.count} readOnly hidden/> 
                  <input name={"Pictures[" + index + "].value"} ref={register({
                  validate: value => value !== "admin" || "Nice try!"})} type="checkbox" /> 
                  Fish on picture
                </div>
              );
            })}
            {/* <img className="picture" src={pictures} aria-hidden='' alt='' /> */}
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
      </div>
    </div>
  );
}

// const Picture = ({url,index}) => {
//   return (
//     <div className='flex-item'>
//       <img className="picture" src={url} aria-hidden='' alt='' /><br/>
//       <input name={"Pictures[" + index + "].url"} type="text" hidden/> 
//       <input name={"Pictures[" + index + "].value"} type="checkbox" /> 
//       Fish on picture
//     </div>
//   )
//   ;
// }

function hexToBase64(str) {
  return btoa(String.fromCharCode.apply(null, str.replace(/\r|\n/g, "").replace(/([\da-fA-F]{2}) ?/g, "0x$1 ").replace(/ +$/, "").split(" ")));
}

export default App;
