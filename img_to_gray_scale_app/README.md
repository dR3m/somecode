# Image to Gray Scale convert REST service (on Django)

Just test app on Django.
Repo including Dockerfile to fast build app.

#### POST req with params in JSON to sent imgs. 
Required params: images links, parameters for cutting off the W/B level.
Responce: id of result imgs.
Example of request:
    body = {'img': {'url': img_link, 'param': WB_lvl }})
    requests.post('http://localhost:8080', data=body)

#### GET req with guid param to get img
Responce: result image with  specified uid. 
