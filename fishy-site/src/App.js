import React, { useState, useEffect } from 'react';
import useForm from "react-hook-form";
import './App.css';

function App() {
  const { handleSubmit, register, errors } = useForm({});
  const [hasError, setErrors] = useState(false);
  const [pictures, setPlanets] = useState({});

  async function fetchData() {
    const res = await fetch("https://swapi.co/api/planets/4/");
    res
      .json()
      .then(res => {

        }
        )
      .catch(err => setErrors(err));
  }

  var demoPictures = {"Pictures": ["/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png","/hej.png"]}

  useEffect(() =>
    {fetchData()}
  , []);

  const onSubmit = values => console.log(values);

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
            {demoPictures.Pictures.map(function(name, index){
              return (
                <div key={index} className='flex-item'>
                  <img className="picture" src={name} aria-hidden='' alt='' /><br/>
                  <input name={"Pictures[" + index + "].url"} type="text" hidden/> 
                  <input name={"Pictures[" + index + "].value"} ref={register({
                  validate: value => value !== "admin" || "Nice try!"})} type="checkbox" /> 
                  Fish on picture
                </div>
              );
            })}
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

export default App;
