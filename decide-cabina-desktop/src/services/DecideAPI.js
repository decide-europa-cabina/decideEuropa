const API_URL = "http://decide-europa-cabina.herokuapp.com";

async function getVotings() {
  return await fetch(API_URL + "/voting", {
    method: "GET"
  }).then(res => res.json());
}

function login(loginForm) {
  return new Promise((resolve, reject) => {
    fetch(API_URL + "/authentication/login/", {
      method: "POST",
      body: JSON.stringify(loginForm),
      headers: {
        "Content-type": "application/json"
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.token === undefined) {
          reject(data);
        } else {
          var auth = { token: data.token };

          fetch(API_URL + "/authentication/getuser/", {
            method: "POST",
            body: JSON.stringify(auth),
            headers: {
              "Content-type": "application/json"
            }
          })
            .then(res => res.json())
            .then(userDetails => {
              auth = { ...auth, id: userDetails.id };
              resolve(auth);
            })
            .catch(err => reject(err));
        }
      })
      .catch(err => reject(err));
  });
}

function vote(auth, votingId, cipher) {
  return new Promise((resolve, reject) => {
    fetch(API_URL + "/store/", {
      method: "POST",
      body: JSON.stringify({
        vote: { a: "", b: "" },
        voting: votingId,
        voter: auth.id,
        token: auth.token
      }),
      headers: {
        "Content-type": "application/json",
        Authorization: "Token " + auth.token
      }
    })
      .then(async res => {
        if (res.status !== 200) {
          reject("Ha habido algún problema");
        } else {
          resolve();
        }
      })
      .catch(err => this.setState({ ...this.state, err: err }));
  });
}

export { getVotings, login, vote };
