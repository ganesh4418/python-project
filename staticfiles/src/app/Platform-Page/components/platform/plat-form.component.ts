import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from 'src/app/shared/user-service.service';
import { PlatformService } from 'src/app/shared/api-serviceEndpoint/platform.service';
import { Platform } from 'src/app/models/platform';
import { LoginUserDetail } from 'src/app/models/user';

class ImageSnippet {
  constructor(public src: string, public file: File) {}
}


@Component({
  selector: 'app-plat-form',
  templateUrl: './plat-form.component.html',
  styleUrls: ['./plat-form.component.css']
})
export class PlatFormComponent implements OnInit {

  username!: string;
  selectedImage: File | undefined;
  imageUrl: string | null = null;
  imagePreview: any;
  user: LoginUserDetail | undefined;
  selectedFile: ImageSnippet | undefined;
  base64Content: string = "";
  platformData: Platform = new Platform();
  selectedIndustry: string[] = [];
  selectedMarketInsight: string = "";

  @ViewChild("dailyInsight") dailyInsight!: ElementRef;
  @ViewChild("weeklyInsight") weeklyInsight!: ElementRef;
  @ViewChild("biweeklyInsight") biweeklyInsight!: ElementRef;
  @ViewChild("monthlyInsight") monthlyInsight !: ElementRef;

  constructor(private userService: UserService, private route: Router, private service: PlatformService) { }

  ngOnInit(): void {
    this.userService.isUserLoggedIn$.subscribe((res) => {
      if (!res) {
        this.route.navigate([""]);
        return;
      }
    })

    this.user = this.userService.userLoginData;
    this.getUserCustomizedInsights();
    const user_id = this.user!.user_id;
    this.getUserProfile(user_id);
  }

  getUserCustomizedInsights() {
    this.service.getUserCustomizedInsights(this.user!.user_id).subscribe(res => {
      if (res && res.user == this.user!.user_id && (res.finance || res.healthcare || res.technology)) {
        if (!this.userService.isUserProfileClicked)
          this.route.navigate(['research']);
      }
    });
  }

  profileUpload(event: any): void {

    const file: File = event.files[0];
    const reader = new FileReader();

    reader.addEventListener('load', (event: any) => {

      this.selectedFile = new ImageSnippet(event.target.result, file);
      this.imagePreview = event.target.value;
      this.service.uploadImage(this.selectedFile.file, this.user!.user_id).subscribe(
        (res : any) => {
        this.imagePreview = res.data.profile_photo;
        },
        (err) => {
        })
    });

    reader.readAsDataURL(file);
    // this.getUserProfile();
  }

  getUserProfile(user_id : any){
    this.service.getProfileImage(user_id).subscribe((img : any)=>{
      this.imagePreview = img.profile_photo;
    })
  }

  downloadImage() {
    const blobData = this.convertBase64ToBlobData(this.base64Content);
  }

  convertBase64ToBlobData(base64Data: string, contentType: string = 'image/png', sliceSize = 512) {
    const byteCharacters = atob(base64Data);
    const byteArrays = [];

    for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
      const slice = byteCharacters.slice(offset, offset + sliceSize);

      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }

      const byteArray = new Uint8Array(byteNumbers);

      byteArrays.push(byteArray);
    }

    const blob = new Blob(byteArrays, { type: contentType });
    return blob;
  }

  industryClicked(event: any, industry: string) {
    if (!(event.target?.parentElement?.classList.contains('focus'))) {
      event.target.parentElement.classList.add('focus');
      event.target.classList.add('focus-text');
      this.selectedIndustry.push(industry);
    }
    else {
      event.target.parentElement.classList.remove('focus');
      event.target.classList.remove('focus-text');
      this.selectedIndustry.splice(this.selectedIndustry.findIndex(x => x == industry), 1);
    }

    console.log('si', this.selectedIndustry);
    this.updateIndustryMarketInsight();
  }

  marketInsightClicked(event: any, market: string) {
    if (this.dailyInsight.nativeElement.parentElement.classList.contains('focus')) {
      this.dailyInsight.nativeElement.parentElement.classList.remove('focus');
      this.dailyInsight.nativeElement.classList.remove('focus-text');
      this.selectedMarketInsight = ""

      if (event.target.text.toLowerCase() === this.dailyInsight.nativeElement.text.toLowerCase()) {
        event.target.parentElement.classList.add('focus');
        event.target.classList.add('focus-text');
        this.selectedMarketInsight = market;
      }
    }

    if (this.weeklyInsight.nativeElement.parentElement.classList.contains('focus')) {
      this.weeklyInsight.nativeElement.parentElement.classList.remove('focus');
      this.weeklyInsight.nativeElement.classList.remove('focus-text');
      this.selectedMarketInsight = "";

      if (event.target.text.toLowerCase() === this.weeklyInsight.nativeElement.text.toLowerCase()) {
        event.target.parentElement.classList.add('focus');
        event.target.classList.add('focus-text');
        this.selectedMarketInsight = market;
      }
    }

    if (this.biweeklyInsight.nativeElement.parentElement.classList.contains('focus')) {
      this.biweeklyInsight.nativeElement.parentElement.classList.remove('focus');
      this.biweeklyInsight.nativeElement.classList.remove('focus-text');
      this.selectedMarketInsight = "";

      if (event.target.text.toLowerCase() === this.biweeklyInsight.nativeElement.text.toLowerCase()) {
        event.target.parentElement.classList.add('focus');
        event.target.classList.add('focus-text');
        this.selectedMarketInsight = market;
      }
    }

    if (this.monthlyInsight.nativeElement.parentElement.classList.contains('focus')) {
      this.monthlyInsight.nativeElement.parentElement.classList.remove('focus');
      this.monthlyInsight.nativeElement.classList.remove('focus-text');
      this.selectedMarketInsight = "";

      if (event.target.text.toLowerCase() === this.monthlyInsight.nativeElement.text.toLowerCase()) {
        event.target.parentElement.classList.add('focus');
        event.target.classList.add('focus-text');
        this.selectedMarketInsight = market;
      }
    }

    if (!(event.target.parentElement.classList.contains('focus'))) {
      event.target.parentElement.classList.add('focus');
      event.target.classList.add('focus-text');
      this.selectedMarketInsight = market;
    } else {
      event.target.parentElement.classList.remove('focus');
      event.target.classList.remove('focus-text');
      this.selectedMarketInsight = "";
    }


    // if (!(event.target.parentElement.classList.contains('focus'))) {
    //   event.target.parentElement.classList.add('focus');
    //   event.target.classList.add('focus-text');
    //   this.selectedMarketInsight = market;
    // } else {
    //   event.target.parentElement.classList.remove('focus');
    //   event.target.classList.remove('focus-text');
    //   this.selectedMarketInsight = "";
    // }
    this.updatePlatformData();
  }

  updateIndustryMarketInsight() {
    this.platformData = new Platform();
    this.selectedIndustry.forEach((s: string) => {
      if (s == "finance")
        this.platformData![s] = true;
      else if (s == "healthcare")
        this.platformData![s] = true;
      else if (s == "technology")
        this.platformData![s] = true;
    });
    this.updatePlatformData();
  }

  updatePlatformData() {
    if ((this.platformData.finance || this.platformData.healthcare || this.platformData.technology) && this.selectedMarketInsight != "") {
      this.platformData.refresh_frequency = this.selectedMarketInsight;
      this.platformData.user = this.userService.userLoginData.user_id;
      this.service.updatePlatformData(this.platformData).subscribe(res => {
        console.log('res', res);
        this.route.navigate(['research']);
      });
    }
  }

  // onUpload(): void {
  //   if (this.selectedFile) {
  //     this.fileUploadService.uploadFile(this.selectedFile).subscribe((response: any) => {
  //       console.log('File uploaded successfully', response);
  //     });
  //   }
  // }

}
