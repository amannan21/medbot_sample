var backend_base_url = 'http://127.0.0.1:5000'//'http://spnayakexplorecsr-env.eba-x6m4uruh.us-east-1.elasticbeanstalk.com'  //

var google_base_url = 'https://www.google.com/search'

document.getElementById("base-form-id").addEventListener(type = "submit",function(event){event.preventDefault()});

function handleSubmit()
{
    console.log('In handle submit');

    try
    {
        $('#response-div-id').remove();
    }catch{}

    let data = document.getElementById('user-text-ip').value;

    let url_to_send = backend_base_url + '/getData?' + (new URLSearchParams({'data' : data})).toString()

    console.log(url_to_send)

    axios.get(url_to_send)
    .then(
        (res) => {
            console.log(res.data);
            createResponse(res.data);
        }
    )
}

function createResponse(data)
{
    let responseDiv = document.createElement('div');
    responseDiv.setAttribute('class', 'response-div');
    responseDiv.setAttribute('id', 'response-div-id');

    let responseTitleDiv = document.createElement('div');
    responseTitleDiv.setAttribute('class', 'response-title');
    
    let cardContainerDiv = null;

    if(data?.count == null || data?.count == undefined || data?.count == 0)
    {
        responseTitleDiv.innerText = 'No Matches Found';
    }

    else
    {
        responseTitleDiv.innerText = 'Matching Diseases';

        cardContainerDiv = document.createElement('div');
        cardContainerDiv.setAttribute('class', 'card-container');

        for(let x of data.disease_list)
        {
            let diseaseDiv = document.createElement('div');
            diseaseDiv.setAttribute('class', 'card');
            
            let diseaseTitleContainer = document.createElement('p');
            diseaseTitleContainer.setAttribute('class', 'disease-title-container');
            let diseaseTitle = document.createElement('a');
            diseaseTitle.value = x?.name;
            diseaseTitle.setAttribute('class', 'disease-title');
            diseaseTitle.setAttribute('target', '_blank');
            diseaseTitle.setAttribute('href', google_base_url + '?' + (new URLSearchParams({'q' : x?.name})).toString());
            diseaseTitle.innerText = x?.name;
            diseaseTitleContainer.appendChild(diseaseTitle);

            let diseaseSimilarityScore = document.createElement('p');
            diseaseSimilarityScore.setAttribute('class', 'disease-similarity-score');
            diseaseSimilarityScore.innerText = 'Similarity Score : ' + x?.similarity_score;

            let symptomList = document.createElement('ul');

            for(let symptom of x?.symptom_list)
            {
                let item = document.createElement('li');
                item.innerText = symptom;
                symptomList.appendChild(item);
            }

            diseaseDiv.appendChild(diseaseTitleContainer);
            diseaseDiv.appendChild(diseaseSimilarityScore);
            diseaseDiv.appendChild(symptomList);

            cardContainerDiv.appendChild(diseaseDiv);
        }
    }

    responseDiv.appendChild(responseTitleDiv);

    if(cardContainerDiv)
    {
        responseDiv.appendChild(cardContainerDiv);
    }

    $('body').append(responseDiv);

    $('#response-div-id')[0].scrollIntoView({behavior : 'smooth'});

}

function handleClear()
{
    console.log('In Clear');

    $('#response-div-id').remove();
    $('#user-text-ip').val('');
}