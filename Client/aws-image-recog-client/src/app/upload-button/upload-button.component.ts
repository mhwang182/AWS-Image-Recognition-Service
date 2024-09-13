import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'upload-button',
  standalone: true,
  imports: [],
  templateUrl: './upload-button.component.html',
  styleUrl: './upload-button.component.scss'
})
export class UploadButtonComponent {
  constructor(private apiService: ApiService) { }

  fileToUpload: File | null = null;

  onFileChange(event: any): void {
    console.log(event);
    this.fileToUpload = <File>event.target.files[0]
  }

  submit(): void {
    console.log('hello world')
    if (!this.fileToUpload) {
      return;
    }

    this.apiService.getUploadLink(this.fileToUpload);
  }
}
