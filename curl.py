import subprocess

def extract_html(url):
    # curl command to retrieve a webpage
    curl_command = ['curl', url]

    # execute the curl command and capture the output
    output = subprocess.check_output(curl_command)

    # print the output
    # with open("curl.txt", "w") as f:
    #     f.write(output.decode())
    return(output.decode())
    #print(output.decode())

#print(extract_html("https://www.bloomberg.com/news/articles/2023-04-19/spotify-chief-goes-to-washington-in-his-crusade-against-apple"))