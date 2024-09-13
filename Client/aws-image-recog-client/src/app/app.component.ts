import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UploadButtonComponent } from './upload-button/upload-button.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, UploadButtonComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'aws-image-recog-client';


}
