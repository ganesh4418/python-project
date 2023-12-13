import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { Platform, ResearchAssistant, TrendingHeadline } from 'src/app/models/platform';
import { environment } from 'src/environments/environment';
import { UserService } from '../user-service.service';


@Injectable({
  providedIn: 'root'
})
export class PlatformService {

  envUrl = environment.apiUrl;
  // researchMenuInvoked$ = new BehaviorSubject<boolean>(false);

  constructor(private httpClient: HttpClient) { }

  getUserCustomizedInsights(userId: number): Observable<Platform> {
    return this.httpClient.get<Platform>(this.envUrl + 'customize_insights/' + userId + '/');
  }

  researchAssistant(userId:number,data: any, trnType: string): Observable<any> {
    if (trnType == "get")
      return this.httpClient.get<any>(this.envUrl + 'inputs-report-generation/' + userId + '/');

    else if (trnType == "post")
      return this.httpClient.post<any>(this.envUrl + 'inputs-report-generation/', data);

    else if (trnType == "put")
      return this.httpClient.put<any>(this.envUrl + 'inputs-report-generation/' + userId + '/', data);

    return of(1);
  }

  updatePlatformData(data: any): Observable<any> {
    return this.httpClient.post(this.envUrl + 'customize_insights/', data);
  }

  uploadImage(file: File, userId: number): Observable<Response> {
    const formData = new FormData();
    const blob = new Blob([file], { type: file.type });
    formData.append('profile_photo', blob, file.name);
    return this.httpClient.put<Response>(this.envUrl + 'user-profile/' + userId + '/photo/', formData);
  }

  getProfileImage(userID:any):Observable<any>{
    console.log(userID);
    
    return this.httpClient.get<any>(this.envUrl + 'user-profile/' + userID + '/photo/')
  }

  getTrendingHeadlines(): Observable<TrendingHeadline> {
    return this.httpClient.get<TrendingHeadline>(this.envUrl + 'trending-headlines/');
  }
}
