import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ResearchAssistant, TrendingHeadlineItem } from 'src/app/models/platform';
import { LoginUserDetail } from 'src/app/models/user';
import { PlatformService } from 'src/app/shared/api-serviceEndpoint/platform.service';
import { UserService } from 'src/app/shared/user-service.service';

@Component({
  selector: 'app-research',
  templateUrl: './research.component.html',
  styleUrls: ['./research.component.css']
})
export class ResearchComponent {

  loaderDisplay: boolean = false;
  isLoading: boolean = false;
  loadingText: string = 'Loading...';

  trendingHeadlinesHide: boolean = false;
  selectedFile: File | null | undefined;
  fileName: string = "";
  getInsightsClicked: boolean = false;
  userData: LoginUserDetail = {} as LoginUserDetail;
  goalWordsGiven: number = 0;
  researchWordsGiven: number = 0;
  parameterWordsGiven: number = 0;
  editResearchClick: boolean = false;
  userInsightExist: boolean = false;
  aiEngineResponse: string = "";
  trendingHeadlineList: TrendingHeadlineItem[] = [];

  @ViewChild('goalInput') goalInput: ElementRef | undefined;
  @ViewChild('researchInput') researchInput: ElementRef | undefined;
  @ViewChild('parameters') parameters: ElementRef | undefined;


  constructor(private userService: UserService, private route: Router, private service: PlatformService) {
    this.form.valueChanges.subscribe(value => {
      this.goalInput!.nativeElement.style.height = 'auto';
      this.goalInput!.nativeElement.style.height = `${this.goalInput!.nativeElement.scrollHeight}px`;

      this.researchInput!.nativeElement.style.height = 'auto';
      this.researchInput!.nativeElement.style.height = `${this.researchInput!.nativeElement.scrollHeight}px`;

      this.parameters!.nativeElement.style.height = 'auto';
      this.parameters!.nativeElement.style.height = `${this.parameters!.nativeElement.scrollHeight}px`;

      this.goalWordsGiven = (this.form.controls.goal.value! && this.form.controls.goal.value!.split("").length > 0 && this.form.controls.goal.value!.split(" ").length > 0) ? this.form.controls.goal.value!.split(" ").length : 0;
      this.researchWordsGiven = (this.form.controls.objects.value! && this.form.controls.objects.value!.split("").length > 0 && this.form.controls.objects.value!.split(" ").length > 0) ? this.form.controls.objects.value!.split(" ").length : 0;
      this.parameterWordsGiven = (this.form.controls.parameters.value! && this.form.controls.parameters.value!.split("").length > 0 && this.form.controls.parameters.value!.split(" ").length > 0) ? this.form.controls.parameters.value!.split(" ").length : 0;
    });

  }

  ngOnInit() {
    this.userService.researchMenuInvoked$.next(true);
    this.userInsightExist = false;
    this.editResearchClick = false;
    this.userService.isUserLoggedIn$.next(true);
    this.userService.isUserLoggedIn$.subscribe((res) => {
      if (!res) {
        this.route.navigate([""]);
        return;
      }
    });
    this.userData = this.userService.userLoginData;
    this.getUserInsights();
    this.getTrendingHeadlineData();

  }

  form = new FormGroup({
    goal: new FormControl('', [Validators.required,Validators.maxLength(500),Validators.max(500)]),
    objects: new FormControl('', [Validators.required,]),
    parameters: new FormControl('', [Validators.required]),
    uploadedFileFormat: new FormControl('', [Validators.required]),
    uploadFile: new FormControl('')
  });

  get researchForm() {
    return this.form.controls;
  }

  getUserInsights() {
    let researchAssistantData: ResearchAssistant = {} as ResearchAssistant;
    researchAssistantData.user = this.userData.user_id;
    const userId = this.userData.user_id;
    this.service.researchAssistant(userId,researchAssistantData, "get").subscribe((res: ResearchAssistant) => {
      if (res.user && res.user > 0) {
        this.userInsightExist = true;
        if (this.editResearchClick)
          this.fillUserResearchData(res);
      }
    });
  }

  fillUserResearchData(data: ResearchAssistant) {
    this.form.patchValue({
      goal: data.research_goal,
      objects: data.research_objective,
      parameters: data.research_parameters,
      uploadedFileFormat: data.report_format
    });
  }

  trendingHeadlineDisplay() {
    this.trendingHeadlinesHide = !this.trendingHeadlinesHide;
  }

  moreInsightsUpload(event: any) {
    console.log('e', event.target.value);
    this.selectedFile = event.target.files[0];
    this.fileName = this.selectedFile!.name;
  }

  removeFile() {
    this.selectedFile = null;
    this.fileName = "";
  }

  uploadFile() {
  }

  inputFieldWordCount(inputField: string) {
    switch (inputField) {
      case "goal": {
        if (this.form.get('goal')!.value!.toString().split(" ").length > 500) {
          this.form.controls['goal'].setErrors({ maxWords: true })
        } else {
          if (this.form.controls['goal'].hasError('maxWords'))
            delete this.form.controls['goal'].errors!['maxWords']
        }
        break;
      }
      case "objects": {
        if (this.form.get('objects')!.value!.toString().split(" ").length > 500) {
          this.form.controls['objects'].setErrors({ maxWords: true })
        } else {
          if (this.form.controls['objects'].hasError('maxWords'))
            delete this.form.controls['objects'].errors!['maxWords']
        }
        break;
      }
      case "parameters": {
        if (this.form.get('parameters')!.value!.toString().split(" ").length > 500) {
          this.form.controls['parameters'].setErrors({ maxWords: true })
        } else {
          if (this.form.controls['parameters'].hasError('maxWords'))
            delete this.form.controls['parameters'].errors!['maxWords']
        }
        break;
      }
    }
    this.form.updateValueAndValidity();
  }

  editResearchClicked() {
    this.getInsightsClicked = false;
    this.editResearchClick = true;
    this.trendingHeadlinesHide = false;
    this.getUserInsights();
  }
  getTrendingHeadlineData() {
    this.service.getTrendingHeadlines().subscribe({
      next: (res) => {
        if (res && res.trending_headlines.length > 0) {
          this.trendingHeadlineList = res.trending_headlines;          
        }
      },
      error: (err) => {
        alert(err.error.error);
      }
    });
  }

  cancelClicked() {
    this.form.reset();
    this.goalWordsGiven = 0;
    this.researchWordsGiven = 0;
    this.parameterWordsGiven = 0;
  }

  getInsights() {
    if (this.form.valid) {
    const user_id = this.userData.user_id;
    const formData = new FormData();
    formData.append('user',user_id.toString())
    formData.append('report_format',this.form.get('uploadedFileFormat')!.value!)
    formData.append('research_goal',this.form.get('goal')!.value!)
    formData.append('research_objective',this.form.get('objects')!.value!)
    formData.append('research_parameters',this.form.get('parameters')!.value!)
    let userId : number = this.userData.user_id;
    let optType: string = this.userInsightExist ? "put" : "post";
    console.log(formData)


    this.loaderDisplay = true;
    this.service.researchAssistant(userId,formData, optType).subscribe((res: any) => {
      this.loaderDisplay = false;
      console.log('res', res);
      this.trendingHeadlinesHide = false;
      alert('request sent');
      this.getInsightsClicked = true;
      this.aiEngineResponse = res.report_result;
      this.form.reset();
    });
    }
    
  }
}

