import React, { useState, useEffect } from 'react';
import useForm from "react-hook-form";
import './App.css';

function App() {
  const { handleSubmit, register, errors } = useForm({});
  const [hasError, setErrors] = useState(false);
  const [pictures, setPictures] = useState({"Pictures": []});
  
  async function fetchData() {
    await fetch("http://127.0.0.1:5900/", {
      headers: {
        'Cache-Control': 'no-cache'
      }
    }).then(
      function(response){
        response
          .json()
          .then(res => {
            console.log(res);
            // console.log("data:image/jpeg;base64," + hexToBase64(res));  
            // var hej = new Blob([res], {type: "image/jpeg"})
            // let fileReader = new FileReader();
            // fileReader.readAsDataURL(res); 
            // fileReader.onload = () => { 
            //   let result = fileReader.result; 
            //   console.log(result); 
            //   setPictures(oldArray => [...oldArray, {result, count}]);
            // }; 
            setPictures(res)
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
        fetchData()
    }
  , []);
  
  //setPictures({"Pictures": som})

  const onSubmit = values => {
    console.log(values)
    fetch('http://127.0.0.1:5900/', {
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
      </header>
      <div className="row">
      <div className="col-sm-2">
      </div>
      <div className="col-sm-8">
      <h1>Do pictures contain fish or not</h1>
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="flex-container">
            {pictures.Pictures.map(function(stuff, index){
              return (
                <div key={index} className='flex-item'>
                  <img className="picture" src={stuff[1]} aria-hidden='' alt='' /><br/>
                  <input name={"Pictures[" + index + "].filename"} ref={register({validate: value => value.String})} value={stuff[0]} readOnly hidden/> 
                  <input name={"Pictures[" + index + "].fishCorrectOnpicture"} ref={register({
                  validate: value => value !== "admin" || "Nice try!"})} type="checkbox" /> 
                  All fish label correctly on picture<br/>
                  <input name={"Pictures[" + index + "].background"} ref={register({
                  validate: value => value !== "somethign" || "like this"})} type="checkbox" /> 
                  No fish on picture
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
