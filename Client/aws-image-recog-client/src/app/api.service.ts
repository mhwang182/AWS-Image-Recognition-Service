import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) {
  }

  async getUploadLink(file: File) {
    console.log(file.name)
    console.log(encodeURIComponent(file.type))
    const fileType = encodeURIComponent(file.type);

    try {

      const headers =
      {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET"
      }
      this.http
        .get(`${this.apiUrl}/upload-link?filename=${file.name}&ext=${fileType}`)
        .subscribe(signedUrl => {
          console.log(signedUrl);
          try {
            this.http
              .put(
                signedUrl as string,
                file,
                { headers }
              ).subscribe(res => console.log(res));
          } catch (error) {
            console.log(error)
          }

        });
    } catch (error) {
      console.log(error);
    }
  }

}


