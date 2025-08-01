
import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Embedded AI Forecast Bot", layout="wide")
st.title("📊 Embedded AI Forecast Bot (24-Month Forecast)")

# --- Embedded Historical CSV Data ---
csv_data = """Month,Customer,Part No,Firm Schedule Qty,Actual Lifting Qty,Gap (Qty),Gap (%),Final product uasage,Supplying country
2023-04-01,"Case New Holland,India",7500000385,30.0,29,-1.0,-0.033333333333333326,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-05-01,"Case New Holland,India",7500000385,30.0,7,-23.0,-0.7666666666666666,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-06-01,"Case New Holland,India",7500000385,46.0,47,1.0,0.021739130434782705,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-07-01,"Case New Holland,India",7500000385,64.0,65,1.0,0.015625,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-08-01,"Case New Holland,India",7500000385,52.0,28,-24.0,-0.46153846153846156,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-09-01,"Case New Holland,India",7500000385,50.0,54,4.0,0.08000000000000007,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-10-01,"Case New Holland,India",7500000385,26.0,38,12.0,0.46153846153846145,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-11-01,"Case New Holland,India",7500000385,90.0,98,8.0,0.0888888888888888,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-12-01,"Case New Holland,India",7500000385,80.0,74,-6.0,-0.07499999999999996,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-01-01,"Case New Holland,India",7500000385,63.0,31,-32.0,-0.5079365079365079,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-02-01,"Case New Holland,India",7500000385,46.0,36,-10.0,-0.21739130434782605,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-03-01,"Case New Holland,India",7500000385,24.0,19,-5.0,-0.20833333333333337,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-04-01,"Case New Holland,India",7500000385,80.0,86,6.0,0.07499999999999996,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-05-01,"Case New Holland,India",7500000385,172.0,162,-10.0,-0.05813953488372092,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-06-01,"Case New Holland,India",7500000385,124.0,113,-11.0,-0.08870967741935487,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-07-01,"Case New Holland,India",7500000385,110.0,127,17.0,0.15454545454545454,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-08-01,"Case New Holland,India",7500000385,122.0,108,-14.0,-0.11475409836065575,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-09-01,"Case New Holland,India",7500000385,100.0,84,-16.0,-0.16000000000000003,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-10-01,"Case New Holland,India",7500000385,114.0,76,-38.0,-0.33333333333333337,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-11-01,"Case New Holland,India",7500000385,64.0,59,-5.0,-0.078125,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-12-01,"Case New Holland,India",7500000385,51.0,30,-21.0,-0.4117647058823529,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-01-01,"Case New Holland,India",7500000385,84.0,81,-3.0,-0.0357142857142857,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-02-01,"Case New Holland,India",7500000385,114.0,106,-8.0,-0.07017543859649122,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-03-01,"Case New Holland,India",7500000385,46.0,28,-18.0,-0.3913043478260869,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-04-01,"Case New Holland,India",7500000385,,103,,,,
2025-05-01,"Case New Holland,India",7500000385,,56,,,,
2025-06-01,"Case New Holland,India",7500000385,,94,,,,
2023-04-01,"Case New Holland,India",7500000384,178.0,148,-30.0,-0.1685393258426966,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-05-01,"Case New Holland,India",7500000384,136.0,118,-18.0,-0.13235294117647056,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-06-01,"Case New Holland,India",7500000384,162.0,143,-19.0,-0.11728395061728392,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-07-01,"Case New Holland,India",7500000384,200.0,186,-14.0,-0.06999999999999995,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-08-01,"Case New Holland,India",7500000384,156.0,123,-33.0,-0.21153846153846156,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-09-01,"Case New Holland,India",7500000384,198.0,192,-6.0,-0.030303030303030276,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-10-01,"Case New Holland,India",7500000384,138.0,129,-9.0,-0.06521739130434778,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-11-01,"Case New Holland,India",7500000384,122.0,115,-7.0,-0.05737704918032782,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-12-01,"Case New Holland,India",7500000384,126.0,122,-4.0,-0.031746031746031744,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-01-01,"Case New Holland,India",7500000384,81.0,48,-33.0,-0.40740740740740744,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-02-01,"Case New Holland,India",7500000384,36.0,24,-12.0,-0.33333333333333337,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-03-01,"Case New Holland,India",7500000384,66.0,69,3.0,0.045454545454545414,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-04-01,"Case New Holland,India",7500000384,66.0,53,-13.0,-0.19696969696969702,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-05-01,"Case New Holland,India",7500000384,102.0,73,-29.0,-0.28431372549019607,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-06-01,"Case New Holland,India",7500000384,90.0,104,14.0,0.15555555555555545,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-07-01,"Case New Holland,India",7500000384,80.0,97,17.0,0.2124999999999999,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-08-01,"Case New Holland,India",7500000384,96.0,93,-3.0,-0.03125,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-09-01,"Case New Holland,India",7500000384,90.0,80,-10.0,-0.11111111111111116,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-10-01,"Case New Holland,India",7500000384,79.0,70,-9.0,-0.11392405063291144,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-11-01,"Case New Holland,India",7500000384,63.0,73,10.0,0.15873015873015883,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-12-01,"Case New Holland,India",7500000384,90.0,81,-9.0,-0.09999999999999998,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-01-01,"Case New Holland,India",7500000384,162.0,157,-5.0,-0.030864197530864224,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-02-01,"Case New Holland,India",7500000384,146.0,119,-27.0,-0.18493150684931503,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-03-01,"Case New Holland,India",7500000384,142.0,130,-12.0,-0.08450704225352113,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-04-01,"Case New Holland,India",7500000384,,85,,,,
2025-05-01,"Case New Holland,India",7500000384,,117,,,,
2025-06-01,"Case New Holland,India",7500000384,,76,,,,
2023-04-01,"Case New Holland,India",7500000381,12.0,0,-12.0,-1.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-05-01,"Case New Holland,India",7500000381,0.0,5,5.0,5.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-06-01,"Case New Holland,India",7500000381,200.0,195,-5.0,-0.025000000000000022,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-07-01,"Case New Holland,India",7500000381,160.0,129,-31.0,-0.19374999999999998,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-08-01,"Case New Holland,India",7500000381,148.0,93,-55.0,-0.3716216216216216,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-09-01,"Case New Holland,India",7500000381,164.0,205,41.0,0.25,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-10-01,"Case New Holland,India",7500000381,216.0,187,-29.0,-0.1342592592592593,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-11-01,"Case New Holland,India",7500000381,160.0,122,-38.0,-0.23750000000000004,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-12-01,"Case New Holland,India",7500000381,84.0,67,-17.0,-0.20238095238095233,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-01-01,"Case New Holland,India",7500000381,172.0,273,101.0,0.5872093023255813,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-02-01,"Case New Holland,India",7500000381,260.0,230,-30.0,-0.11538461538461542,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-03-01,"Case New Holland,India",7500000381,170.0,140,-30.0,-0.17647058823529416,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-04-01,"Case New Holland,India",7500000381,72.0,82,10.0,0.13888888888888884,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-05-01,"Case New Holland,India",7500000381,120.0,122,2.0,0.016666666666666607,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-06-01,"Case New Holland,India",7500000381,149.0,126,-23.0,-0.15436241610738255,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-07-01,"Case New Holland,India",7500000381,160.0,147,-13.0,-0.08125000000000004,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-08-01,"Case New Holland,India",7500000381,170.0,160,-10.0,-0.05882352941176472,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-09-01,"Case New Holland,India",7500000381,218.0,209,-9.0,-0.041284403669724745,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-10-01,"Case New Holland,India",7500000381,254.0,263,9.0,0.03543307086614167,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-11-01,"Case New Holland,India",7500000381,272.0,260,-12.0,-0.044117647058823484,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-12-01,"Case New Holland,India",7500000381,236.0,236,0.0,0.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-01-01,"Case New Holland,India",7500000381,0.0,5,5.0,5.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-02-01,"Case New Holland,India",7500000381,0.0,3,3.0,3.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-03-01,"Case New Holland,India",7500000381,2.0,5,3.0,1.5,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-04-01,"Case New Holland,India",7500000381,,4,,,,
2025-05-01,"Case New Holland,India",7500000381,,8,,,,
2025-06-01,"Case New Holland,India",7500000381,,4,,,,
2023-04-01,"Case New Holland,India",7500000380,36.0,33,-3.0,-0.08333333333333337,"Construction,landscaping and Utility",India
2023-05-01,"Case New Holland,India",7500000380,42.0,33,-9.0,-0.2142857142857143,"Construction,landscaping and Utility",India
2023-06-01,"Case New Holland,India",7500000380,36.0,24,-12.0,-0.33333333333333337,"Construction,landscaping and Utility",India
2023-07-01,"Case New Holland,India",7500000380,24.0,9,-15.0,-0.625,"Construction,landscaping and Utility",India
2023-08-01,"Case New Holland,India",7500000380,22.0,16,-6.0,-0.2727272727272727,"Construction,landscaping and Utility",India
2023-09-01,"Case New Holland,India",7500000380,28.0,25,-3.0,-0.1071428571428571,"Construction,landscaping and Utility",India
2023-10-01,"Case New Holland,India",7500000380,18.0,22,4.0,0.22222222222222232,"Construction,landscaping and Utility",India
2023-11-01,"Case New Holland,India",7500000380,12.0,5,-7.0,-0.5833333333333333,"Construction,landscaping and Utility",India
2023-12-01,"Case New Holland,India",7500000380,18.0,13,-5.0,-0.2777777777777778,"Construction,landscaping and Utility",India
2024-01-01,"Case New Holland,India",7500000380,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",India
2024-02-01,"Case New Holland,India",7500000380,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",India
2024-03-01,"Case New Holland,India",7500000380,0.0,0,0.0,0.0,"Construction,landscaping and Utility",India
2024-04-01,"Case New Holland,India",7500000380,0.0,0,0.0,0.0,"Construction,landscaping and Utility",India
2024-05-01,"Case New Holland,India",7500000380,7.0,6,-1.0,-0.1428571428571429,"Construction,landscaping and Utility",India
2024-06-01,"Case New Holland,India",7500000380,9.0,7,-2.0,-0.2222222222222222,"Construction,landscaping and Utility",India
2024-07-01,"Case New Holland,India",7500000380,14.0,12,-2.0,-0.1428571428571429,"Construction,landscaping and Utility",India
2024-08-01,"Case New Holland,India",7500000380,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",India
2024-09-01,"Case New Holland,India",7500000380,4.0,3,-1.0,-0.25,"Construction,landscaping and Utility",India
2024-10-01,"Case New Holland,India",7500000380,2.0,2,0.0,0.0,"Construction,landscaping and Utility",India
2024-11-01,"Case New Holland,India",7500000380,6.0,6,0.0,0.0,"Construction,landscaping and Utility",India
2024-12-01,"Case New Holland,India",7500000380,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",India
2025-01-01,"Case New Holland,India",7500000380,28.0,23,-5.0,-0.1785714285714286,"Construction,landscaping and Utility",India
2025-02-01,"Case New Holland,India",7500000380,28.0,18,-10.0,-0.3571428571428571,"Construction,landscaping and Utility",India
2025-03-01,"Case New Holland,India",7500000380,16.0,8,-8.0,-0.5,"Construction,landscaping and Utility",India
2025-04-01,"Case New Holland,India",7500000380,,16,,,,
2025-05-01,"Case New Holland,India",7500000380,,16,,,,
2025-06-01,"Case New Holland,India",7500000380,,13,,,,
2023-04-01,"Case New Holland,India",7500000835,40.0,31,-9.0,-0.22499999999999998,"Construction,landscaping and Utility",India
2023-05-01,"Case New Holland,India",7500000835,30.0,39,9.0,0.30000000000000004,"Construction,landscaping and Utility",India
2023-06-01,"Case New Holland,India",7500000835,52.0,40,-12.0,-0.23076923076923073,"Construction,landscaping and Utility",India
2023-07-01,"Case New Holland,India",7500000835,38.0,36,-2.0,-0.052631578947368474,"Construction,landscaping and Utility",India
2023-08-01,"Case New Holland,India",7500000835,44.0,34,-10.0,-0.2272727272727273,"Construction,landscaping and Utility",India
2023-09-01,"Case New Holland,India",7500000835,44.0,42,-2.0,-0.045454545454545414,"Construction,landscaping and Utility",India
2023-10-01,"Case New Holland,India",7500000835,72.0,73,1.0,0.01388888888888884,"Construction,landscaping and Utility",India
2023-11-01,"Case New Holland,India",7500000835,20.0,24,4.0,0.19999999999999996,"Construction,landscaping and Utility",India
2023-12-01,"Case New Holland,India",7500000835,34.0,24,-10.0,-0.2941176470588235,"Construction,landscaping and Utility",India
2024-01-01,"Case New Holland,India",7500000835,46.0,19,-27.0,-0.5869565217391304,"Construction,landscaping and Utility",India
2024-02-01,"Case New Holland,India",7500000835,58.0,57,-1.0,-0.017241379310344862,"Construction,landscaping and Utility",India
2024-03-01,"Case New Holland,India",7500000835,96.0,95,-1.0,-0.01041666666666663,"Construction,landscaping and Utility",India
2024-04-01,"Case New Holland,India",7500000835,104.0,86,-18.0,-0.17307692307692313,"Construction,landscaping and Utility",India
2024-05-01,"Case New Holland,India",7500000835,90.0,71,-19.0,-0.21111111111111114,"Construction,landscaping and Utility",India
2024-06-01,"Case New Holland,India",7500000835,50.0,79,29.0,0.5800000000000001,"Construction,landscaping and Utility",India
2024-07-01,"Case New Holland,India",7500000835,126.0,108,-18.0,-0.1428571428571429,"Construction,landscaping and Utility",India
2024-08-01,"Case New Holland,India",7500000835,55.0,35,-20.0,-0.36363636363636365,"Construction,landscaping and Utility",India
2024-09-01,"Case New Holland,India",7500000835,6.0,6,0.0,0.0,"Construction,landscaping and Utility",India
2024-10-01,"Case New Holland,India",7500000835,8.0,4,-4.0,-0.5,"Construction,landscaping and Utility",India
2024-11-01,"Case New Holland,India",7500000835,24.0,24,0.0,0.0,"Construction,landscaping and Utility",India
2024-12-01,"Case New Holland,India",7500000835,66.0,35,-31.0,-0.4696969696969697,"Construction,landscaping and Utility",India
2025-01-01,"Case New Holland,India",7500000835,44.0,44,0.0,0.0,"Construction,landscaping and Utility",India
2025-02-01,"Case New Holland,India",7500000835,10.0,29,19.0,1.9,"Construction,landscaping and Utility",India
2025-03-01,"Case New Holland,India",7500000835,10.0,7,-3.0,-0.30000000000000004,"Construction,landscaping and Utility",India
2025-04-01,"Case New Holland,India",7500000835,,26,,,,
2025-05-01,"Case New Holland,India",7500000835,,8,,,,
2025-06-01,"Case New Holland,India",7500000835,,33,,,,
2023-04-01,"Case New Holland,India",7500000831,72.0,76,4.0,0.05555555555555558,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-05-01,"Case New Holland,India",7500000831,80.0,78,-2.0,-0.025000000000000022,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-06-01,"Case New Holland,India",7500000831,80.0,83,3.0,0.03750000000000009,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-07-01,"Case New Holland,India",7500000831,48.0,43,-5.0,-0.10416666666666663,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-08-01,"Case New Holland,India",7500000831,14.0,7,-7.0,-0.5,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-09-01,"Case New Holland,India",7500000831,26.0,31,5.0,0.1923076923076923,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-10-01,"Case New Holland,India",7500000831,36.0,15,-21.0,-0.5833333333333333,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-11-01,"Case New Holland,India",7500000831,0.0,3,3.0,3.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2023-12-01,"Case New Holland,India",7500000831,0.0,2,2.0,2.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-01-01,"Case New Holland,India",7500000831,4.5,2,-2.5,-0.5555555555555556,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-02-01,"Case New Holland,India",7500000831,9.0,6,-3.0,-0.33333333333333337,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-03-01,"Case New Holland,India",7500000831,16.0,6,-10.0,-0.625,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-04-01,"Case New Holland,India",7500000831,5.0,2,-3.0,-0.6,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-05-01,"Case New Holland,India",7500000831,6.0,11,5.0,0.8333333333333333,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-06-01,"Case New Holland,India",7500000831,18.0,16,-2.0,-0.11111111111111116,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-07-01,"Case New Holland,India",7500000831,8.0,5,-3.0,-0.375,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-08-01,"Case New Holland,India",7500000831,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-09-01,"Case New Holland,India",7500000831,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-10-01,"Case New Holland,India",7500000831,0.0,2,2.0,2.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-11-01,"Case New Holland,India",7500000831,1.0,7,6.0,6.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2024-12-01,"Case New Holland,India",7500000831,0.0,14,14.0,14.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-01-01,"Case New Holland,India",7500000831,13.0,8,-5.0,-0.3846153846153846,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-02-01,"Case New Holland,India",7500000831,10.0,15,5.0,0.5,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-03-01,"Case New Holland,India",7500000831,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility","India,Gulf countries,South africa,Ukrain,rasia,malesia,Asia pacefic"
2025-04-01,"Case New Holland,India",7500000831,,0,,,,
2025-05-01,"Case New Holland,India",7500000831,,0,,,,
2025-06-01,"Case New Holland,India",7500000831,,0,,,,
2023-04-01,"Case New Holland,India",7500001538,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001538,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001538,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001538,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001538,6.0,3,-3.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001538,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001538,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001538,2.0,1,-1.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001538,1.0,0,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001538,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001538,6.0,5,-1.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001538,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001538,34.0,25,-9.0,-0.2647058823529412,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001538,36.0,0,-36.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001538,,83,,,,
2025-05-01,"Case New Holland,India",7500001538,,98,,,,
2025-06-01,"Case New Holland,India",7500001538,,126,,,,
2023-04-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001776,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001776,12.0,15,3.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001776,30.0,25,-5.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001776,10.0,5,-5.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001776,9.0,13,4.0,0.4444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001776,9.0,8,-1.0,-0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001776,8.0,8,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001776,20.0,15,-5.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001776,15.0,1,-14.0,-0.9333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001776,10.0,8,-2.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001776,12.0,5,-7.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001776,8.0,4,-4.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001776,14.0,12,-2.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001776,14.0,12,-2.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001776,22.0,13,-9.0,-0.4090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001776,2.0,1,-1.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001776,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001776,,1,,,,
2025-05-01,"Case New Holland,India",7500001776,,1,,,,
2025-06-01,"Case New Holland,India",7500001776,,1,,,,
2023-04-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001704,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001704,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001704,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001704,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001704,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001704,2.0,1,-1.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001704,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001704,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001704,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001704,0.0,18,18.0,18.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001704,0.0,41,41.0,41.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001704,0.0,38,38.0,38.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001704,,27,,,,
2025-05-01,"Case New Holland,India",7500001704,,13,,,,
2025-06-01,"Case New Holland,India",7500001704,,26,,,,
2023-04-01,"Case New Holland,India",7500000834,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000834,8.0,9,1.0,0.125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000834,12.0,10,-2.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000834,8.0,8,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000834,7.0,6,-1.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000834,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000834,12.0,8,-4.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000834,0.0,6,6.0,6.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000834,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000834,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000834,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000834,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000834,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000834,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000834,,3,,,,
2025-05-01,"Case New Holland,India",7500000834,,1,,,,
2025-06-01,"Case New Holland,India",7500000834,,0,,,,
2023-04-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001885,12.0,13,1.0,0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001885,56.0,44,-12.0,-0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001885,56.0,53,-3.0,-0.05357142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001885,28.0,1,-27.0,-0.9642857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001885,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001885,26.0,34,8.0,0.3076923076923077,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001885,12.0,1,-11.0,-0.9166666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001885,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001885,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001885,1.0,1,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001885,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001885,1.0,1,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001885,,0,,,,
2025-05-01,"Case New Holland,India",7500001885,,0,,,,
2025-06-01,"Case New Holland,India",7500001885,,0,,,,
2023-04-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000867,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000867,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000867,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000867,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000867,4.0,1,-3.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000867,2.0,1,-1.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000867,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000867,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000867,6.0,3,-3.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000867,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000867,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000867,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000867,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000867,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000867,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000867,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000867,,2,,,,
2025-05-01,"Case New Holland,India",7500000867,,2,,,,
2025-06-01,"Case New Holland,India",7500000867,,2,,,,
2023-04-01,"Case New Holland,India",7500000524,24.0,21,-3.0,-0.125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000524,24.0,24,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000524,14.0,9,-5.0,-0.35714285714285715,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000524,18.0,18,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000524,15.0,10,-5.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000524,30.0,29,-1.0,-0.03333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000524,30.0,25,-5.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000524,34.0,29,-5.0,-0.14705882352941177,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000524,50.0,40,-10.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000524,50.0,40,-10.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000524,50.0,40,-10.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000524,28.0,21,-7.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000524,28.0,34,6.0,0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000524,36.0,32,-4.0,-0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000524,20.0,19,-1.0,-0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000524,25.0,21,-4.0,-0.16,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000524,45.0,43,-2.0,-0.044444444444444446,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000524,45.0,42,-3.0,-0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000524,54.0,47,-7.0,-0.12962962962962962,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000524,54.0,44,-10.0,-0.18518518518518517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000524,49.0,56,7.0,0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000524,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000524,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000524,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000524,,0,,,,
2025-05-01,"Case New Holland,India",7500000524,,0,,,,
2025-06-01,"Case New Holland,India",7500000524,,1,,,,
2023-04-01,"Case New Holland,India",7500000328,36.0,33,-3.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000328,42.0,33,-9.0,-0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000328,36.0,24,-12.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000328,24.0,10,-14.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000328,22.0,16,-6.0,-0.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000328,28.0,25,-3.0,-0.10714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000328,18.0,22,4.0,0.2222222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000328,12.0,5,-7.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000328,20.0,13,-7.0,-0.35,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000328,11.0,0,-11.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000328,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000328,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000328,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000328,7.0,8,1.0,0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000328,6.0,7,1.0,0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000328,14.0,12,-2.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000328,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000328,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000328,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000328,6.0,6,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000328,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000328,28.0,22,-6.0,-0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000328,28.0,20,-8.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000328,16.0,8,-8.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000328,,16,,,,
2025-05-01,"Case New Holland,India",7500000328,,16,,,,
2025-06-01,"Case New Holland,India",7500000328,,13,,,,
2023-04-01,"Case New Holland,India",7500000850,27.0,20,-7.0,-0.25925925925925924,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000850,28.0,24,-4.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000850,20.0,18,-2.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000850,17.0,12,-5.0,-0.29411764705882354,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000850,18.0,12,-6.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000850,34.0,26,-8.0,-0.23529411764705882,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000850,35.0,0,-35.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000850,50.0,29,-21.0,-0.42,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000850,66.0,39,-27.0,-0.4090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000850,60.0,41,-19.0,-0.31666666666666665,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000850,64.0,35,-29.0,-0.453125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000850,51.0,22,-29.0,-0.5686274509803921,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000850,40.0,32,-8.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000850,50.0,38,-12.0,-0.24,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000850,32.0,17,-15.0,-0.46875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000850,26.0,17,-9.0,-0.34615384615384615,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000850,50.0,45,-5.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000850,50.0,42,-8.0,-0.16,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000850,52.0,45,-7.0,-0.1346153846153846,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000850,58.0,47,-11.0,-0.1896551724137931,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000850,60.0,55,-5.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000850,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000850,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000850,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000850,,0,,,,
2025-05-01,"Case New Holland,India",7500000850,,0,,,,
2025-06-01,"Case New Holland,India",7500000850,,0,,,,
2023-04-01,"Case New Holland,India",7500000640,87.0,32,-55.0,-0.632183908045977,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000640,90.0,46,-44.0,-0.4888888888888889,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000640,90.0,50,-40.0,-0.4444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000640,75.0,80,5.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000640,100.0,32,-68.0,-0.68,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000640,100.0,58,-42.0,-0.42,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000640,100.0,60,-40.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000640,130.0,80,-50.0,-0.38461538461538464,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000640,136.0,116,-20.0,-0.14705882352941177,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000640,50.0,22,-28.0,-0.56,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000640,60.0,62,2.0,0.03333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000640,100.0,80,-20.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000640,110.0,112,2.0,0.01818181818181818,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000640,130.0,40,-90.0,-0.6923076923076923,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000640,130.0,102,-28.0,-0.2153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000640,128.0,56,-72.0,-0.5625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000640,150.0,72,-78.0,-0.52,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000640,150.0,116,-34.0,-0.22666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000640,150.0,84,-66.0,-0.44,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000640,100.0,88,-12.0,-0.12,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000640,82.0,88,6.0,0.07317073170731707,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000640,34.0,56,22.0,0.6470588235294118,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000640,40.0,30,-10.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000640,44.0,15,-29.0,-0.6590909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000640,,56,,,,
2025-05-01,"Case New Holland,India",7500000640,,108,,,,
2025-06-01,"Case New Holland,India",7500000640,,78,,,,
2023-04-01,"Case New Holland,India",7500000849,27.0,20,-7.0,-0.25925925925925924,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000849,28.0,24,-4.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000849,20.0,18,-2.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000849,17.0,12,-5.0,-0.29411764705882354,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000849,18.0,13,-5.0,-0.2777777777777778,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000849,34.0,26,-8.0,-0.23529411764705882,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000849,35.0,33,-2.0,-0.05714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000849,50.0,29,-21.0,-0.42,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000849,66.0,39,-27.0,-0.4090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000849,60.0,41,-19.0,-0.31666666666666665,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000849,63.0,35,-28.0,-0.4444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000849,51.0,22,-29.0,-0.5686274509803921,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000849,40.0,32,-8.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000849,50.0,38,-12.0,-0.24,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000849,32.0,17,-15.0,-0.46875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000849,26.0,18,-8.0,-0.3076923076923077,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000849,50.0,46,-4.0,-0.08,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000849,50.0,42,-8.0,-0.16,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000849,52.0,45,-7.0,-0.1346153846153846,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000849,58.0,47,-11.0,-0.1896551724137931,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000849,60.0,57,-3.0,-0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000849,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000849,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000849,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000849,,0,,,,
2025-05-01,"Case New Holland,India",7500000849,,0,,,,
2025-06-01,"Case New Holland,India",7500000849,,0,,,,
2023-04-01,"Case New Holland,India",7500000441,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000441,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000441,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000441,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000441,1.0,0,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000441,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000441,5.0,5,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000441,4.0,3,-1.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000441,6.0,5,-1.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000441,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000441,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000441,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000441,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000441,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000441,8.0,5,-3.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000441,7.0,3,-4.0,-0.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000441,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000441,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000441,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000441,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000441,1.0,0,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000441,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000441,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000441,3.0,1,-2.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000441,,2,,,,
2025-05-01,"Case New Holland,India",7500000441,,1,,,,
2025-06-01,"Case New Holland,India",7500000441,,1,,,,
2023-04-01,"Case New Holland,India",7500000445,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000445,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000445,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000445,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000445,1.0,0,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000445,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000445,5.0,5,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000445,4.0,3,-1.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000445,6.0,5,-1.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000445,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000445,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000445,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000445,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000445,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000445,8.0,5,-3.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000445,7.0,3,-4.0,-0.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000445,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000445,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000445,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000445,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000445,1.0,0,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000445,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000445,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000445,3.0,1,-2.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000445,,2,,,,
2025-05-01,"Case New Holland,India",7500000445,,1,,,,
2025-06-01,"Case New Holland,India",7500000445,,1,,,,
2023-04-01,"Case New Holland,India",7500001048,80.0,24,-56.0,-0.7,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001048,20.0,72,52.0,2.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001048,70.0,64,-6.0,-0.08571428571428572,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001048,0.0,24,24.0,24.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001048,0.0,28,28.0,28.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001048,0.0,48,48.0,48.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001048,0.0,88,88.0,88.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001048,0.0,52,52.0,52.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001048,0.0,52,52.0,52.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001048,0.0,160,160.0,160.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001048,0.0,96,96.0,96.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001048,0.0,112,112.0,112.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001048,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001048,0.0,64,64.0,64.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001048,0.0,56,56.0,56.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001048,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001048,0.0,60,60.0,60.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001048,0.0,142,142.0,142.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001048,0.0,160,160.0,160.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001048,0.0,96,96.0,96.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001048,0.0,160,160.0,160.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001048,0.0,80,80.0,80.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001048,0.0,80,80.0,80.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001048,0.0,96,96.0,96.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001048,,96,,,,
2025-05-01,"Case New Holland,India",7500001048,,88,,,,
2025-06-01,"Case New Holland,India",7500001048,,88,,,,
2023-04-01,"Case New Holland,India",7500001625,29.0,0,-29.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001625,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001625,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001625,43.0,0,-43.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001625,48.0,0,-48.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001625,32.0,0,-32.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001625,32.0,4,-28.0,-0.875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001625,68.0,0,-68.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001625,91.0,0,-91.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001625,182.0,0,-182.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001625,193.0,0,-193.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001625,200.0,0,-200.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001625,200.0,0,-200.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001625,243.0,0,-243.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001625,240.0,0,-240.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001625,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001625,80.0,0,-80.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001625,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001625,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001625,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001625,26.0,0,-26.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001625,12.0,0,-12.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001625,26.0,0,-26.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001625,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001625,,0,,,,
2025-05-01,"Case New Holland,India",7500001625,,0,,,,
2025-06-01,"Case New Holland,India",7500001625,,0,,,,
2023-04-01,"Case New Holland,India",7500000395,35.0,28,-7.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000395,30.0,29,-1.0,-0.03333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000395,30.0,24,-6.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000395,25.0,22,-3.0,-0.12,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000395,42.0,33,-9.0,-0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000395,30.0,28,-2.0,-0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000395,40.0,41,1.0,0.025,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000395,50.0,15,-35.0,-0.7,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000395,65.0,57,-8.0,-0.12307692307692308,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000395,59.0,58,-1.0,-0.01694915254237288,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000395,60.0,46,-14.0,-0.23333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000395,72.0,46,-26.0,-0.3611111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000395,65.0,48,-17.0,-0.26153846153846155,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000395,75.0,51,-24.0,-0.32,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000395,70.0,48,-22.0,-0.3142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000395,79.0,58,-21.0,-0.26582278481012656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000395,70.0,50,-20.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000395,60.0,42,-18.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000395,61.0,53,-8.0,-0.13114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000395,70.0,71,1.0,0.014285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000395,70.0,67,-3.0,-0.04285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000395,0.0,-1,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000395,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000395,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000395,,0,,,,
2025-05-01,"Case New Holland,India",7500000395,,0,,,,
2025-06-01,"Case New Holland,India",7500000395,,0,,,,
2023-04-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000315,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000315,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000315,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000315,6.0,1,-5.0,-0.8333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000315,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000315,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000315,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000315,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000315,2.0,1,-1.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000315,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000315,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000315,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000315,,0,,,,
2025-05-01,"Case New Holland,India",7500000315,,0,,,,
2025-06-01,"Case New Holland,India",7500000315,,0,,,,
2023-04-01,"Case New Holland,India",7500000314,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000314,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000314,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000314,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000314,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000314,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000314,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000314,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000314,6.0,1,-5.0,-0.8333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000314,5.0,5,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000314,5.0,2,-3.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000314,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000314,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000314,10.0,6,-4.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000314,7.0,2,-5.0,-0.7142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000314,9.0,2,-7.0,-0.7777777777777778,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000314,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000314,3.0,4,1.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000314,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000314,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000314,7.0,0,-7.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000314,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000314,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000314,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000314,,2,,,,
2025-05-01,"Case New Holland,India",7500000314,,4,,,,
2025-06-01,"Case New Holland,India",7500000314,,0,,,,
2023-04-01,"Case New Holland,India",7500000460,29.0,27,-2.0,-0.06896551724137931,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000460,31.0,17,-14.0,-0.45161290322580644,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000460,15.0,15,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000460,19.0,14,-5.0,-0.2631578947368421,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000460,15.0,15,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000460,34.0,17,-17.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000460,40.0,34,-6.0,-0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000460,58.0,32,-26.0,-0.4482758620689655,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000460,55.0,30,-25.0,-0.45454545454545453,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000460,70.0,46,-24.0,-0.34285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000460,68.0,59,-9.0,-0.1323529411764706,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000460,60.0,20,-40.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000460,50.0,33,-17.0,-0.34,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000460,70.0,19,-51.0,-0.7285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000460,35.0,22,-13.0,-0.37142857142857144,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000460,33.0,22,-11.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000460,60.0,33,-27.0,-0.45,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000460,50.0,34,-16.0,-0.32,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000460,54.0,46,-8.0,-0.14814814814814814,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000460,58.0,42,-16.0,-0.27586206896551724,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000460,56.0,56,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000460,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000460,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000460,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000460,,0,,,,
2025-05-01,"Case New Holland,India",7500000460,,0,,,,
2025-06-01,"Case New Holland,India",7500000460,,0,,,,
2023-04-01,"Case New Holland,India",7500000327,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000327,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000327,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000327,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000327,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000327,0.0,1,1.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000327,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000327,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000327,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000327,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000327,-2.0,0,2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000327,0.0,4,4.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000327,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000327,10.0,2,-8.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000327,7.0,2,-5.0,-0.7142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000327,9.0,0,-9.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000327,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000327,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000327,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000327,6.0,2,-4.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000327,5.0,1,-4.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000327,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000327,3.0,1,-2.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000327,4.0,2,-2.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000327,,2,,,,
2025-05-01,"Case New Holland,India",7500000327,,4,,,,
2025-06-01,"Case New Holland,India",7500000327,,1,,,,
2023-04-01,"Case New Holland,India",7500000394,35.0,28,-7.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000394,30.0,29,-1.0,-0.03333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000394,30.0,24,-6.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000394,25.0,22,-3.0,-0.12,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000394,42.0,33,-9.0,-0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000394,30.0,28,-2.0,-0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000394,45.0,41,-4.0,-0.08888888888888889,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000394,55.0,15,-40.0,-0.7272727272727273,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000394,65.0,56,-9.0,-0.13846153846153847,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000394,59.0,56,-3.0,-0.05084745762711865,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000394,60.0,46,-14.0,-0.23333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000394,72.0,46,-26.0,-0.3611111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000394,65.0,48,-17.0,-0.26153846153846155,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000394,75.0,51,-24.0,-0.32,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000394,70.0,48,-22.0,-0.3142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000394,79.0,54,-25.0,-0.31645569620253167,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000394,70.0,50,-20.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000394,60.0,42,-18.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000394,61.0,49,-12.0,-0.19672131147540983,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000394,70.0,71,1.0,0.014285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000394,70.0,67,-3.0,-0.04285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000394,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000394,0.0,-1,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000394,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000394,,0,,,,
2025-05-01,"Case New Holland,India",7500000394,,0,,,,
2025-06-01,"Case New Holland,India",7500000394,,0,,,,
2023-04-01,"Case New Holland,India",7500000346,56.0,40,-16.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000346,60.0,53,-7.0,-0.11666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000346,70.0,64,-6.0,-0.08571428571428572,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000346,102.0,64,-38.0,-0.37254901960784315,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000346,40.0,25,-15.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000346,67.0,49,-18.0,-0.26865671641791045,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000346,50.0,35,-15.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000346,73.0,15,-58.0,-0.7945205479452054,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000346,20.0,5,-15.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000346,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000346,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000346,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000346,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000346,5.0,5,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000346,16.0,10,-6.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000346,19.0,10,-9.0,-0.47368421052631576,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000346,1.0,1,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000346,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000346,2.0,4,2.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000346,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000346,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000346,26.0,29,3.0,0.11538461538461539,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000346,30.0,15,-15.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000346,20.0,11,-9.0,-0.45,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000346,,19,,,,
2025-05-01,"Case New Holland,India",7500000346,,18,,,,
2025-06-01,"Case New Holland,India",7500000346,,22,,,,
2023-04-01,"Case New Holland,India",7500000819,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000819,10.0,9,-1.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000819,45.0,51,6.0,0.13333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000819,59.0,40,-19.0,-0.3220338983050847,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000819,60.0,32,-28.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000819,60.0,54,-6.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000819,60.0,55,-5.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000819,65.0,20,-45.0,-0.6923076923076923,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000819,20.0,9,-11.0,-0.55,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000819,55.0,55,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000819,55.0,39,-16.0,-0.2909090909090909,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000819,81.0,60,-21.0,-0.25925925925925924,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000819,60.0,55,-5.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000819,70.0,59,-11.0,-0.15714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000819,60.0,46,-14.0,-0.23333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000819,54.0,52,-2.0,-0.037037037037037035,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000819,40.0,14,-26.0,-0.65,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000819,60.0,40,-20.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000819,70.0,54,-16.0,-0.22857142857142856,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000819,50.0,51,1.0,0.02,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000819,55.0,54,-1.0,-0.01818181818181818,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000819,26.0,0,-26.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000819,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000819,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000819,,0,,,,
2025-05-01,"Case New Holland,India",7500000819,,0,,,,
2025-06-01,"Case New Holland,India",7500000819,,0,,,,
2023-04-01,"Case New Holland,India",7500000822,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000822,10.0,9,-1.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000822,45.0,51,6.0,0.13333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000822,59.0,40,-19.0,-0.3220338983050847,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000822,60.0,32,-28.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000822,60.0,54,-6.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000822,60.0,57,-3.0,-0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000822,63.0,20,-43.0,-0.6825396825396826,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000822,20.0,9,-11.0,-0.55,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000822,55.0,55,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000822,55.0,44,-11.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000822,81.0,60,-21.0,-0.25925925925925924,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000822,60.0,55,-5.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000822,70.0,59,-11.0,-0.15714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000822,60.0,46,-14.0,-0.23333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000822,54.0,52,-2.0,-0.037037037037037035,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000822,40.0,14,-26.0,-0.65,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000822,60.0,40,-20.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000822,70.0,54,-16.0,-0.22857142857142856,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000822,50.0,51,1.0,0.02,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000822,55.0,54,-1.0,-0.01818181818181818,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000822,26.0,0,-26.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000822,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000822,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000822,,0,,,,
2025-05-01,"Case New Holland,India",7500000822,,0,,,,
2025-06-01,"Case New Holland,India",7500000822,,0,,,,
2023-04-01,"Case New Holland,India",7500000823,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000823,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000823,12.0,0,-12.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000823,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000823,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000823,12.0,14,2.0,0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000823,15.0,10,-5.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000823,15.0,10,-5.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000823,20.0,10,-10.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000823,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000823,12.0,10,-2.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000823,13.0,5,-8.0,-0.6153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000823,11.0,10,-1.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000823,12.0,5,-7.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000823,20.0,19,-1.0,-0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000823,39.0,20,-19.0,-0.48717948717948717,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000823,10.0,9,-1.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000823,0.0,4,4.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000823,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000823,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000823,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000823,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000823,4.0,1,-3.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000823,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000823,,3,,,,
2025-05-01,"Case New Holland,India",7500000823,,5,,,,
2025-06-01,"Case New Holland,India",7500000823,,2,,,,
2023-04-01,"Case New Holland,India",7500000358,56.0,40,-16.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000358,60.0,53,-7.0,-0.11666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000358,70.0,64,-6.0,-0.08571428571428572,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000358,102.0,64,-38.0,-0.37254901960784315,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000358,40.0,25,-15.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000358,67.0,53,-14.0,-0.208955223880597,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000358,50.0,36,-14.0,-0.28,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000358,68.0,15,-53.0,-0.7794117647058824,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000358,20.0,5,-15.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000358,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000358,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000358,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000358,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000358,5.0,5,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000358,16.0,10,-6.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000358,19.0,10,-9.0,-0.47368421052631576,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000358,1.0,1,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000358,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000358,2.0,4,2.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000358,2.0,3,1.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000358,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000358,26.0,29,3.0,0.11538461538461539,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000358,30.0,15,-15.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000358,20.0,11,-9.0,-0.45,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000358,,19,,,,
2025-05-01,"Case New Holland,India",7500000358,,18,,,,
2025-06-01,"Case New Holland,India",7500000358,,22,,,,
2023-04-01,"Case New Holland,India",7500000820,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000820,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000820,12.0,0,-12.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000820,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000820,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000820,12.0,10,-2.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000820,15.0,17,2.0,0.13333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000820,15.0,10,-5.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000820,24.0,10,-14.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000820,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000820,12.0,10,-2.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000820,13.0,5,-8.0,-0.6153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000820,11.0,10,-1.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000820,12.0,5,-7.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000820,16.0,19,3.0,0.1875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000820,39.0,20,-19.0,-0.48717948717948717,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000820,10.0,9,-1.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000820,0.0,4,4.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000820,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000820,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000820,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000820,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000820,4.0,1,-3.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000820,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000820,,3,,,,
2025-05-01,"Case New Holland,India",7500000820,,5,,,,
2025-06-01,"Case New Holland,India",7500000820,,2,,,,
2023-04-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000412,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000412,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000412,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000412,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000412,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000412,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000412,11.0,10,-1.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000412,10.0,5,-5.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000412,5.0,7,2.0,0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000412,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000412,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000412,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000412,,0,,,,
2025-05-01,"Case New Holland,India",7500000412,,5,,,,
2025-06-01,"Case New Holland,India",7500000412,,0,,,,
2023-04-01,"Case New Holland,India",7500000894,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000894,255.0,420,165.0,0.6470588235294118,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000894,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000894,243.0,144,-99.0,-0.4074074074074074,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000894,150.0,5,-145.0,-0.9666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000894,200.0,108,-92.0,-0.46,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000894,220.0,452,232.0,1.0545454545454545,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000894,350.0,383,33.0,0.09428571428571429,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000894,60.0,228,168.0,2.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000894,240.0,226,-14.0,-0.058333333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000894,266.0,-2,-268.0,-1.0075187969924813,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000894,428.0,0,-428.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000894,120.0,270,150.0,1.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000894,60.0,215,155.0,2.5833333333333335,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000894,120.0,0,-120.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000894,280.0,288,8.0,0.02857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000894,200.0,168,-32.0,-0.16,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000894,240.0,220,-20.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000894,290.0,396,106.0,0.36551724137931035,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000894,300.0,120,-180.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000894,360.0,407,47.0,0.13055555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000894,120.0,168,48.0,0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000894,120.0,118,-2.0,-0.016666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000894,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000894,,0,,,,
2025-05-01,"Case New Holland,India",7500000894,,0,,,,
2025-06-01,"Case New Holland,India",7500000894,,0,,,,
2023-04-01,"Case New Holland,India",7500000336,44.0,43,-1.0,-0.022727272727272728,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000336,30.0,43,13.0,0.43333333333333335,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000336,25.0,17,-8.0,-0.32,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000336,30.0,51,21.0,0.7,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000336,24.0,0,-24.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000336,34.0,57,23.0,0.6764705882352942,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000336,26.0,38,12.0,0.46153846153846156,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000336,31.0,0,-31.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000336,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000336,93.0,69,-24.0,-0.25806451612903225,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000336,50.0,4,-46.0,-0.92,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000336,89.0,0,-89.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000336,80.0,56,-24.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000336,68.0,0,-68.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000336,100.0,25,-75.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000336,117.0,91,-26.0,-0.2222222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000336,30.0,68,38.0,1.2666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000336,0.0,39,39.0,39.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000336,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000336,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000336,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000336,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000336,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000336,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000336,,0,,,,
2025-05-01,"Case New Holland,India",7500000336,,17,,,,
2025-06-01,"Case New Holland,India",7500000336,,0,,,,
2023-04-01,"Case New Holland,India",7500000329,87.0,56,-31.0,-0.3563218390804598,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000329,40.0,24,-16.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000329,80.0,47,-33.0,-0.4125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000329,55.0,63,8.0,0.14545454545454545,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000329,75.0,53,-22.0,-0.29333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000329,75.0,42,-33.0,-0.44,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000329,110.0,65,-45.0,-0.4090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000329,160.0,109,-51.0,-0.31875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000329,139.0,45,-94.0,-0.6762589928057554,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000329,40.0,37,-3.0,-0.075,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000329,73.0,60,-13.0,-0.1780821917808219,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000329,150.0,80,-70.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000329,140.0,86,-54.0,-0.38571428571428573,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000329,182.0,99,-83.0,-0.45604395604395603,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000329,120.0,99,-21.0,-0.175,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000329,156.0,131,-25.0,-0.16025641025641027,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000329,60.0,53,-7.0,-0.11666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000329,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000329,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000329,45.0,27,-18.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000329,57.0,48,-9.0,-0.15789473684210525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000329,17.0,34,17.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000329,40.0,39,-1.0,-0.025,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000329,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000329,,30,,,,
2025-05-01,"Case New Holland,India",7500000329,,14,,,,
2025-06-01,"Case New Holland,India",7500000329,,36,,,,
2023-04-01,"Case New Holland,India",7500000636,100.0,110,10.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000636,60.0,32,-28.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000636,20.0,53,33.0,1.65,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000636,102.0,104,2.0,0.0196078431372549,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000636,72.0,135,63.0,0.875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000636,70.0,77,7.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000636,52.0,69,17.0,0.3269230769230769,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000636,62.0,0,-62.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000636,118.0,40,-78.0,-0.6610169491525424,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000636,144.0,65,-79.0,-0.5486111111111112,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000636,131.0,41,-90.0,-0.6870229007633588,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000636,103.0,68,-35.0,-0.33980582524271846,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000636,100.0,89,-11.0,-0.11,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000636,100.0,0,-100.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000636,180.0,69,-111.0,-0.6166666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000636,195.0,125,-70.0,-0.358974358974359,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000636,60.0,33,-27.0,-0.45,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000636,0.0,81,81.0,81.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000636,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000636,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000636,62.0,0,-62.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000636,62.0,0,-62.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000636,122.0,35,-87.0,-0.7131147540983607,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000636,80.0,46,-34.0,-0.425,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000636,,36,,,,
2025-05-01,"Case New Holland,India",7500000636,,9,,,,
2025-06-01,"Case New Holland,India",7500000636,,36,,,,
2023-04-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000538,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000538,4.0,6,2.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000538,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000538,10.0,18,8.0,0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000538,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000538,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000538,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000538,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000538,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000538,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000538,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000538,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000538,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000538,,7,,,,
2025-05-01,"Case New Holland,India",7500000538,,0,,,,
2025-06-01,"Case New Holland,India",7500000538,,0,,,,
2023-04-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000398,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000398,8.0,4,-4.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000398,10.0,11,1.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000398,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000398,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000398,10.0,2,-8.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000398,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000398,20.0,8,-12.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000398,16.0,0,-16.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000398,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000398,20.0,2,-18.0,-0.9,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000398,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000398,7.0,2,-5.0,-0.7142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000398,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000398,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000398,7.0,3,-4.0,-0.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000398,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000398,4.0,3,-1.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000398,,5,,,,
2025-05-01,"Case New Holland,India",7500000398,,0,,,,
2025-06-01,"Case New Holland,India",7500000398,,0,,,,
2023-04-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000428,4.0,6,2.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000428,2.0,5,3.0,1.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000428,10.0,13,3.0,0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000428,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000428,9.0,0,-9.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000428,13.0,0,-13.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000428,17.0,18,1.0,0.058823529411764705,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000428,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000428,2.0,0,-2.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000428,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000428,3.0,0,-3.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000428,,6,,,,
2025-05-01,"Case New Holland,India",7500000428,,0,,,,
2025-06-01,"Case New Holland,India",7500000428,,12,,,,
2023-04-01,"Case New Holland,India",7500000399,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000399,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000399,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000399,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000399,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000399,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000399,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000399,6.0,4,-2.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000399,8.0,11,3.0,0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000399,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000399,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000399,10.0,2,-8.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000399,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000399,20.0,8,-12.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000399,16.0,0,-16.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000399,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000399,20.0,2,-18.0,-0.9,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000399,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000399,7.0,2,-5.0,-0.7142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000399,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000399,7.0,0,-7.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000399,7.0,3,-4.0,-0.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000399,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000399,4.0,3,-1.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000399,,5,,,,
2025-05-01,"Case New Holland,India",7500000399,,2,,,,
2025-06-01,"Case New Holland,India",7500000399,,5,,,,
2023-04-01,"Case New Holland,India",7500000413,32.0,27,-5.0,-0.15625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000413,23.0,10,-13.0,-0.5652173913043478,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000413,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000413,23.0,20,-3.0,-0.13043478260869565,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000413,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000413,34.0,25,-9.0,-0.2647058823529412,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000413,60.0,35,-25.0,-0.4166666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000413,87.0,54,-33.0,-0.3793103448275862,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000413,70.0,34,-36.0,-0.5142857142857142,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000413,86.0,36,-50.0,-0.5813953488372093,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000413,95.0,54,-41.0,-0.43157894736842106,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000413,62.0,24,-38.0,-0.6129032258064516,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000413,30.0,22,-8.0,-0.26666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000413,46.0,43,-3.0,-0.06521739130434782,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000413,20.0,24,4.0,0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000413,16.0,25,9.0,0.5625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000413,40.0,41,1.0,0.025,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000413,30.0,21,-9.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000413,38.0,23,-15.0,-0.39473684210526316,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000413,54.0,24,-30.0,-0.5555555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000413,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000413,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000413,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000413,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000413,,0,,,,
2025-05-01,"Case New Holland,India",7500000413,,0,,,,
2025-06-01,"Case New Holland,India",7500000413,,0,,,,
2023-04-01,"Case New Holland,India",7500000698,100.0,60,-40.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000698,56.0,30,-26.0,-0.4642857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000698,16.0,100,84.0,5.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000698,105.0,104,-1.0,-0.009523809523809525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000698,78.0,80,2.0,0.02564102564102564,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000698,90.0,0,-90.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000698,0.0,80,80.0,80.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000698,100.0,60,-40.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000698,100.0,32,-68.0,-0.68,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000698,70.0,64,-6.0,-0.08571428571428572,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000698,28.0,60,32.0,1.1428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000698,80.0,85,5.0,0.0625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000698,150.0,150,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000698,150.0,57,-93.0,-0.62,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000698,240.0,128,-112.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000698,240.0,125,-115.0,-0.4791666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000698,173.0,0,-173.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000698,60.0,50,-10.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000698,100.0,90,-10.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000698,100.0,70,-30.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000698,76.0,0,-76.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000698,76.0,50,-26.0,-0.34210526315789475,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000698,100.0,45,-55.0,-0.55,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000698,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000698,,47,,,,
2025-05-01,"Case New Holland,India",7500000698,,80,,,,
2025-06-01,"Case New Holland,India",7500000698,,80,,,,
2023-04-01,"Case New Holland,India",7500000457,38.0,38,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000457,24.0,10,-14.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000457,23.0,21,-2.0,-0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000457,30.0,12,-18.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000457,48.0,40,-8.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000457,30.0,20,-10.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000457,60.0,43,-17.0,-0.2833333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000457,62.0,27,-35.0,-0.5645161290322581,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000457,77.0,36,-41.0,-0.5324675324675324,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000457,78.0,53,-25.0,-0.32051282051282054,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000457,72.0,51,-21.0,-0.2916666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000457,82.0,58,-24.0,-0.2926829268292683,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000457,70.0,62,-8.0,-0.11428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000457,70.0,68,-2.0,-0.02857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000457,50.0,39,-11.0,-0.22,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000457,70.0,59,-11.0,-0.15714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000457,70.0,34,-36.0,-0.5142857142857142,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000457,50.0,29,-21.0,-0.42,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000457,61.0,50,-11.0,-0.18032786885245902,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000457,70.0,62,-8.0,-0.11428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000457,67.0,65,-2.0,-0.029850746268656716,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000457,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000457,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000457,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000457,,0,,,,
2025-05-01,"Case New Holland,India",7500000457,,0,,,,
2025-06-01,"Case New Holland,India",7500000457,,0,,,,
2023-04-01,"Case New Holland,India",7500000456,38.0,38,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000456,24.0,10,-14.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000456,23.0,21,-2.0,-0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000456,30.0,12,-18.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000456,48.0,40,-8.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000456,30.0,20,-10.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000456,60.0,43,-17.0,-0.2833333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000456,62.0,27,-35.0,-0.5645161290322581,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000456,77.0,36,-41.0,-0.5324675324675324,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000456,78.0,52,-26.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000456,72.0,50,-22.0,-0.3055555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000456,82.0,58,-24.0,-0.2926829268292683,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000456,70.0,62,-8.0,-0.11428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000456,70.0,68,-2.0,-0.02857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000456,50.0,39,-11.0,-0.22,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000456,70.0,59,-11.0,-0.15714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000456,78.0,34,-44.0,-0.5641025641025641,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000456,50.0,29,-21.0,-0.42,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000456,61.0,50,-11.0,-0.18032786885245902,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000456,70.0,62,-8.0,-0.11428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000456,65.0,65,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000456,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000456,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000456,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000456,,0,,,,
2025-05-01,"Case New Holland,India",7500000456,,0,,,,
2025-06-01,"Case New Holland,India",7500000456,,0,,,,
2023-04-01,"Case New Holland,India",7500000839,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000839,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000839,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000839,23.0,23,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000839,18.0,0,-18.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000839,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000839,60.0,59,-1.0,-0.016666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000839,61.0,80,19.0,0.3114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000839,70.0,38,-32.0,-0.45714285714285713,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000839,90.0,40,-50.0,-0.5555555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000839,94.0,0,-94.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000839,90.0,56,-34.0,-0.37777777777777777,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000839,40.0,0,-40.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000839,68.0,57,-11.0,-0.16176470588235295,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000839,31.0,32,1.0,0.03225806451612903,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000839,27.0,16,-11.0,-0.4074074074074074,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000839,52.0,55,3.0,0.057692307692307696,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000839,13.0,15,2.0,0.15384615384615385,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000839,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000839,21.0,25,4.0,0.19047619047619047,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000839,10.0,11,1.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000839,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000839,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000839,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000839,,0,,,,
2025-05-01,"Case New Holland,India",7500000839,,0,,,,
2025-06-01,"Case New Holland,India",7500000839,,0,,,,
2023-04-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000316,50.0,55,5.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000316,32.0,31,-1.0,-0.03125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000316,29.0,30,1.0,0.034482758620689655,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000316,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000316,30.0,24,-6.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000316,20.0,30,10.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000316,20.0,10,-10.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000316,34.0,32,-2.0,-0.058823529411764705,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000316,0.0,5,5.0,5.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000316,5.0,6,1.0,0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000316,6.0,6,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000316,13.0,13,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000316,0.0,5,5.0,5.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000316,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000316,,0,,,,
2025-05-01,"Case New Holland,India",7500000316,,0,,,,
2025-06-01,"Case New Holland,India",7500000316,,34,,,,
2023-04-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000537,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000537,6.0,4,-2.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000537,10.0,5,-5.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000537,5.0,7,2.0,0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000537,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000537,8.0,5,-3.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000537,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000537,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000537,18.0,0,-18.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000537,5.0,2,-3.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000537,7.0,6,-1.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000537,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000537,7.0,0,-7.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000537,8.0,8,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000537,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000537,,0,,,,
2025-05-01,"Case New Holland,India",7500000537,,2,,,,
2025-06-01,"Case New Holland,India",7500000537,,0,,,,
2023-04-01,"Case New Holland,India",7500000349,100.0,48,-52.0,-0.52,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000349,30.0,21,-9.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000349,40.0,28,-12.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000349,100.0,71,-29.0,-0.29,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000349,100.0,37,-63.0,-0.63,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000349,40.0,57,17.0,0.425,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000349,100.0,34,-66.0,-0.66,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000349,116.0,15,-101.0,-0.8706896551724138,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000349,50.0,16,-34.0,-0.68,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000349,62.0,10,-52.0,-0.8387096774193549,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000349,72.0,0,-72.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000349,62.0,33,-29.0,-0.46774193548387094,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000349,150.0,52,-98.0,-0.6533333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000349,140.0,12,-128.0,-0.9142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000349,200.0,19,-181.0,-0.905,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000349,234.0,86,-148.0,-0.6324786324786325,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000349,100.0,21,-79.0,-0.79,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000349,0.0,22,22.0,22.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000349,50.0,42,-8.0,-0.16,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000349,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000349,39.0,0,-39.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000349,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000349,70.0,14,-56.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000349,100.0,20,-80.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000349,,54,,,,
2025-05-01,"Case New Holland,India",7500000349,,10,,,,
2025-06-01,"Case New Holland,India",7500000349,,47,,,,
2023-04-01,"Case New Holland,India",7500000449,38.0,45,7.0,0.18421052631578946,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000449,24.0,22,-2.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000449,23.0,28,5.0,0.21739130434782608,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000449,30.0,25,-5.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000449,48.0,10,-38.0,-0.7916666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000449,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000449,45.0,49,4.0,0.08888888888888889,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000449,50.0,10,-40.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000449,77.0,64,-13.0,-0.16883116883116883,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000449,55.0,55,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000449,78.0,53,-25.0,-0.32051282051282054,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000449,61.0,35,-26.0,-0.4262295081967213,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000449,84.0,60,-24.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000449,70.0,46,-24.0,-0.34285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000449,70.0,63,-7.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000449,70.0,61,-9.0,-0.12857142857142856,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000449,70.0,28,-42.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000449,50.0,35,-15.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000449,61.0,53,-8.0,-0.13114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000449,70.0,47,-23.0,-0.32857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000449,64.0,66,2.0,0.03125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000449,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000449,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000449,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000449,,0,,,,
2025-05-01,"Case New Holland,India",7500000449,,0,,,,
2025-06-01,"Case New Holland,India",7500000449,,0,,,,
2023-04-01,"Case New Holland,India",7500000669,26.0,50,24.0,0.9230769230769231,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000669,0.0,35,35.0,35.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000669,8.0,80,72.0,9.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000669,30.0,50,20.0,0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000669,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000669,44.0,0,-44.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000669,0.0,-5,-5.0,-5.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000669,44.0,0,-44.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000669,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000669,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000669,31.0,50,19.0,0.6129032258064516,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000669,35.0,30,-5.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000669,62.0,65,3.0,0.04838709677419355,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000669,46.0,78,32.0,0.6956521739130435,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000669,50.0,45,-5.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000669,67.0,50,-17.0,-0.2537313432835821,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000669,20.0,30,10.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000669,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000669,68.0,70,2.0,0.029411764705882353,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000669,48.0,0,-48.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000669,69.0,0,-69.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000669,69.0,0,-69.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000669,70.0,50,-20.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000669,25.0,0,-25.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000669,,8,,,,
2025-05-01,"Case New Holland,India",7500000669,,4,,,,
2025-06-01,"Case New Holland,India",7500000669,,12,,,,
2023-04-01,"Case New Holland,India",7500000700,26.0,50,24.0,0.9230769230769231,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000700,0.0,25,25.0,25.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000700,8.0,80,72.0,9.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000700,30.0,40,10.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000700,26.0,0,-26.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000700,44.0,0,-44.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000700,0.0,-1,-1.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000700,44.0,0,-44.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000700,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000700,44.0,0,-44.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000700,55.0,50,-5.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000700,35.0,30,-5.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000700,150.0,50,-100.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000700,150.0,58,-92.0,-0.6133333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000700,200.0,50,-150.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000700,200.0,80,-120.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000700,120.0,30,-90.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000700,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000700,88.0,90,2.0,0.022727272727272728,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000700,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000700,71.0,0,-71.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000700,40.0,0,-40.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000700,40.0,50,10.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000700,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000700,,50,,,,
2025-05-01,"Case New Holland,India",7500000700,,45,,,,
2025-06-01,"Case New Holland,India",7500000700,,50,,,,
2023-04-01,"Case New Holland,India",7500000335,44.0,65,21.0,0.4772727272727273,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000335,0.0,53,53.0,53.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000335,22.0,0,-22.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000335,30.0,32,2.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000335,20.0,40,20.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000335,40.0,40,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000335,30.0,75,45.0,1.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000335,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000335,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000335,69.0,56,-13.0,-0.18840579710144928,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000335,28.0,72,44.0,1.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000335,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000335,54.0,39,-15.0,-0.2777777777777778,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000335,84.0,62,-22.0,-0.2619047619047619,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000335,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000335,0.0,46,46.0,46.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000335,0.0,24,24.0,24.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000335,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000335,,0,,,,
2025-05-01,"Case New Holland,India",7500000335,,13,,,,
2025-06-01,"Case New Holland,India",7500000335,,35,,,,
2023-04-01,"Case New Holland,India",7500000549,38.0,38,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000549,24.0,21,-3.0,-0.125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000549,23.0,30,7.0,0.30434782608695654,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000549,30.0,15,-15.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000549,48.0,30,-18.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000549,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000549,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000549,55.0,18,-37.0,-0.6727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000549,89.0,43,-46.0,-0.5168539325842697,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000549,73.0,42,-31.0,-0.4246575342465753,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000549,79.0,59,-20.0,-0.25316455696202533,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000549,73.0,42,-31.0,-0.4246575342465753,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000549,70.0,67,-3.0,-0.04285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000549,70.0,31,-39.0,-0.5571428571428572,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000549,90.0,59,-31.0,-0.34444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000549,90.0,49,-41.0,-0.45555555555555555,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000549,88.0,50,-38.0,-0.4318181818181818,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000549,60.0,48,-12.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000549,61.0,42,-19.0,-0.3114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000549,70.0,49,-21.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000549,76.0,79,3.0,0.039473684210526314,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000549,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000549,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000549,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000549,,0,,,,
2025-05-01,"Case New Holland,India",7500000549,,0,,,,
2025-06-01,"Case New Holland,India",7500000549,,3,,,,
2023-04-01,"Case New Holland,India",7500000448,38.0,45,7.0,0.18421052631578946,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000448,24.0,22,-2.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000448,23.0,26,3.0,0.13043478260869565,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000448,30.0,25,-5.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000448,48.0,10,-38.0,-0.7916666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000448,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000448,60.0,49,-11.0,-0.18333333333333332,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000448,61.0,10,-51.0,-0.8360655737704918,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000448,88.0,66,-22.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000448,64.0,52,-12.0,-0.1875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000448,79.0,49,-30.0,-0.379746835443038,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000448,74.0,35,-39.0,-0.527027027027027,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000448,84.0,60,-24.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000448,70.0,46,-24.0,-0.34285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000448,70.0,63,-7.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000448,70.0,61,-9.0,-0.12857142857142856,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000448,70.0,28,-42.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000448,70.0,35,-35.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000448,61.0,53,-8.0,-0.13114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000448,63.0,47,-16.0,-0.25396825396825395,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000448,76.0,66,-10.0,-0.13157894736842105,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000448,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000448,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000448,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000448,,0,,,,
2025-05-01,"Case New Holland,India",7500000448,,0,,,,
2025-06-01,"Case New Holland,India",7500000448,,0,,,,
2023-04-01,"Case New Holland,India",7500000506,39.0,52,13.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000506,46.0,46,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000506,192.0,140,-52.0,-0.2708333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000506,231.0,243,12.0,0.05194805194805195,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000506,220.0,160,-60.0,-0.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000506,200.0,118,-82.0,-0.41,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000506,200.0,140,-60.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000506,332.0,79,-253.0,-0.7620481927710844,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000506,300.0,201,-99.0,-0.33,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000506,358.0,262,-96.0,-0.2681564245810056,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000506,396.0,189,-207.0,-0.5227272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000506,346.0,148,-198.0,-0.5722543352601156,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000506,200.0,143,-57.0,-0.285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000506,179.0,123,-56.0,-0.3128491620111732,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000506,201.0,90,-111.0,-0.5522388059701493,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000506,274.0,109,-165.0,-0.6021897810218978,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000506,313.0,157,-156.0,-0.4984025559105431,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000506,220.0,195,-25.0,-0.11363636363636363,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000506,270.0,157,-113.0,-0.4185185185185185,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000506,300.0,235,-65.0,-0.21666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000506,330.0,273,-57.0,-0.17272727272727273,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000506,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000506,60.0,80,20.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000506,0.0,20,20.0,20.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000506,,54,,,,
2025-05-01,"Case New Holland,India",7500000506,,69,,,,
2025-06-01,"Case New Holland,India",7500000506,,90,,,,
2023-04-01,"Case New Holland,India",7500000423,100.0,94,-6.0,-0.06,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000423,46.0,62,16.0,0.34782608695652173,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000423,192.0,140,-52.0,-0.2708333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000423,231.0,228,-3.0,-0.012987012987012988,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000423,220.0,160,-60.0,-0.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000423,200.0,158,-42.0,-0.21,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000423,200.0,95,-105.0,-0.525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000423,340.0,80,-260.0,-0.7647058823529411,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000423,150.0,205,55.0,0.36666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000423,270.0,263,-7.0,-0.025925925925925925,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000423,249.0,127,-122.0,-0.4899598393574297,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000423,320.0,212,-108.0,-0.3375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000423,170.0,120,-50.0,-0.29411764705882354,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000423,172.0,134,-38.0,-0.22093023255813954,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000423,183.0,95,-88.0,-0.4808743169398907,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000423,274.0,112,-162.0,-0.5912408759124088,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000423,310.0,155,-155.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000423,220.0,200,-20.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000423,266.0,150,-116.0,-0.43609022556390975,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000423,300.0,243,-57.0,-0.19,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000423,330.0,268,-62.0,-0.18787878787878787,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000423,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000423,60.0,80,20.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000423,0.0,20,20.0,20.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000423,,54,,,,
2025-05-01,"Case New Holland,India",7500000423,,75,,,,
2025-06-01,"Case New Holland,India",7500000423,,78,,,,
2023-04-01,"Case New Holland,India",7500000705,100.0,55,-45.0,-0.45,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000705,56.0,50,-6.0,-0.10714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000705,16.0,40,24.0,1.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000705,105.0,120,15.0,0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000705,78.0,20,-58.0,-0.7435897435897436,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000705,100.0,20,-80.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000705,110.0,80,-30.0,-0.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000705,130.0,70,-60.0,-0.46153846153846156,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000705,120.0,85,-35.0,-0.2916666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000705,57.0,50,-7.0,-0.12280701754385964,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000705,29.0,60,31.0,1.0689655172413792,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000705,70.0,100,30.0,0.42857142857142855,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000705,150.0,110,-40.0,-0.26666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000705,150.0,130,-20.0,-0.13333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000705,200.0,135,-65.0,-0.325,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000705,200.0,150,-50.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000705,120.0,75,-45.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000705,0.0,50,50.0,50.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000705,100.0,100,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000705,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000705,96.0,0,-96.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000705,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000705,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000705,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000705,,50,,,,
2025-05-01,"Case New Holland,India",7500000705,,100,,,,
2025-06-01,"Case New Holland,India",7500000705,,50,,,,
2023-04-01,"Case New Holland,India",7500000550,38.0,38,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000550,24.0,20,-4.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000550,23.0,30,7.0,0.30434782608695654,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000550,30.0,15,-15.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000550,48.0,30,-18.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000550,83.0,30,-53.0,-0.6385542168674698,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000550,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000550,55.0,18,-37.0,-0.6727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000550,89.0,43,-46.0,-0.5168539325842697,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000550,73.0,42,-31.0,-0.4246575342465753,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000550,79.0,59,-20.0,-0.25316455696202533,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000550,73.0,33,-40.0,-0.547945205479452,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000550,70.0,66,-4.0,-0.05714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000550,70.0,32,-38.0,-0.5428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000550,90.0,59,-31.0,-0.34444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000550,90.0,49,-41.0,-0.45555555555555555,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000550,88.0,52,-36.0,-0.4090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000550,60.0,48,-12.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000550,61.0,42,-19.0,-0.3114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000550,70.0,49,-21.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000550,76.0,77,1.0,0.013157894736842105,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000550,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000550,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000550,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000550,,1,,,,
2025-05-01,"Case New Holland,India",7500000550,,0,,,,
2025-06-01,"Case New Holland,India",7500000550,,7,,,,
2023-04-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000333,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000333,16.0,0,-16.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000333,24.0,10,-14.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000333,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000333,14.0,5,-9.0,-0.6428571428571429,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000333,9.0,0,-9.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000333,15.0,0,-15.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000333,27.0,0,-27.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000333,35.0,7,-28.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000333,35.0,15,-20.0,-0.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000333,8.0,8,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000333,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000333,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000333,,11,,,,
2025-05-01,"Case New Holland,India",7500000333,,5,,,,
2025-06-01,"Case New Holland,India",7500000333,,2,,,,
2023-04-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000418,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000418,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000418,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000418,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000418,8.0,15,7.0,0.875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000418,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000418,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000418,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000418,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000418,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000418,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000418,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000418,,0,,,,
2025-05-01,"Case New Holland,India",7500000418,,6,,,,
2025-06-01,"Case New Holland,India",7500000418,,0,,,,
2023-04-01,"Case New Holland,India",7500000334,63.0,55,-8.0,-0.12698412698412698,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000334,70.0,59,-11.0,-0.15714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000334,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000334,45.0,8,-37.0,-0.8222222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000334,36.0,39,3.0,0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000334,80.0,38,-42.0,-0.525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000334,180.0,153,-27.0,-0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000334,169.0,40,-129.0,-0.7633136094674556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000334,200.0,58,-142.0,-0.71,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000334,212.0,50,-162.0,-0.7641509433962265,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000334,250.0,56,-194.0,-0.776,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000334,232.0,74,-158.0,-0.6810344827586207,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000334,100.0,95,-5.0,-0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000334,60.0,35,-25.0,-0.4166666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000334,60.0,33,-27.0,-0.45,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000334,77.0,35,-42.0,-0.5454545454545454,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000334,114.0,82,-32.0,-0.2807017543859649,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000334,80.0,76,-4.0,-0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000334,104.0,74,-30.0,-0.28846153846153844,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000334,140.0,119,-21.0,-0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000334,107.0,86,-21.0,-0.19626168224299065,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000334,0.0,4,4.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000334,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000334,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000334,,0,,,,
2025-05-01,"Case New Holland,India",7500000334,,0,,,,
2025-06-01,"Case New Holland,India",7500000334,,0,,,,
2023-04-01,"Case New Holland,India",7500000637,44.0,49,5.0,0.11363636363636363,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000637,30.0,24,-6.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000637,22.0,21,-1.0,-0.045454545454545456,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000637,51.0,51,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000637,0.0,20,20.0,20.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000637,30.0,14,-16.0,-0.5333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000637,30.0,20,-10.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000637,34.0,0,-34.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000637,60.0,21,-39.0,-0.65,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000637,56.0,7,-49.0,-0.875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000637,64.0,0,-64.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000637,72.0,63,-9.0,-0.125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000637,23.0,9,-14.0,-0.6086956521739131,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000637,48.0,0,-48.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000637,78.0,12,-66.0,-0.8461538461538461,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000637,104.0,94,-10.0,-0.09615384615384616,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000637,30.0,19,-11.0,-0.36666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000637,0.0,15,15.0,15.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000637,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000637,24.0,0,-24.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000637,55.0,0,-55.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000637,55.0,24,-31.0,-0.5636363636363636,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000637,53.0,17,-36.0,-0.6792452830188679,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000637,55.0,48,-7.0,-0.12727272727272726,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000637,,16,,,,
2025-05-01,"Case New Holland,India",7500000637,,12,,,,
2025-06-01,"Case New Holland,India",7500000637,,0,,,,
2023-04-01,"Case New Holland,India",7500000414,32.0,28,-4.0,-0.125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000414,23.0,21,-2.0,-0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000414,10.0,7,-3.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000414,27.0,8,-19.0,-0.7037037037037037,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000414,20.0,10,-10.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000414,34.0,40,6.0,0.17647058823529413,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000414,60.0,34,-26.0,-0.43333333333333335,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000414,76.0,30,-46.0,-0.6052631578947368,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000414,91.0,58,-33.0,-0.3626373626373626,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000414,80.0,22,-58.0,-0.725,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000414,102.0,64,-38.0,-0.37254901960784315,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000414,46.0,8,-38.0,-0.8260869565217391,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000414,40.0,20,-20.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000414,79.0,54,-25.0,-0.31645569620253167,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000414,52.0,39,-13.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000414,40.0,42,2.0,0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000414,42.0,42,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000414,43.0,20,-23.0,-0.5348837209302325,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000414,61.0,10,-51.0,-0.8360655737704918,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000414,60.0,30,-30.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000414,45.0,60,15.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000414,2.0,2,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000414,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000414,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000414,,13,,,,
2025-05-01,"Case New Holland,India",7500000414,,0,,,,
2025-06-01,"Case New Holland,India",7500000414,,0,,,,
2023-04-01,"Case New Holland,India",7500000431,32.0,41,9.0,0.28125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000431,23.0,29,6.0,0.2608695652173913,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000431,10.0,2,-8.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000431,23.0,0,-23.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000431,20.0,13,-7.0,-0.35,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000431,34.0,38,4.0,0.11764705882352941,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000431,120.0,74,-46.0,-0.38333333333333336,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000431,186.0,80,-106.0,-0.5698924731182796,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000431,125.0,76,-49.0,-0.392,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000431,94.0,0,-94.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000431,138.0,51,-87.0,-0.6304347826086957,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000431,43.0,5,-38.0,-0.8837209302325582,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000431,40.0,40,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000431,46.0,14,-32.0,-0.6956521739130435,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000431,20.0,10,-10.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000431,30.0,10,-20.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000431,61.0,61,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000431,21.0,16,-5.0,-0.23809523809523808,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000431,50.0,51,1.0,0.02,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000431,20.0,8,-12.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000431,10.0,18,8.0,0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000431,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000431,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000431,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000431,,0,,,,
2025-05-01,"Case New Holland,India",7500000431,,0,,,,
2025-06-01,"Case New Holland,India",7500000431,,0,,,,
2023-04-01,"Case New Holland,India",7500000411,42.0,46,4.0,0.09523809523809523,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000411,38.0,44,6.0,0.15789473684210525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000411,32.0,6,-26.0,-0.8125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000411,29.0,33,4.0,0.13793103448275862,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000411,20.0,15,-5.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000411,31.0,0,-31.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000411,20.0,41,21.0,1.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000411,24.0,8,-16.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000411,22.0,52,30.0,1.3636363636363635,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000411,0.0,28,28.0,28.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000411,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000411,12.0,12,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000411,13.0,15,2.0,0.15384615384615385,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000411,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000411,,0,,,,
2025-05-01,"Case New Holland,India",7500000411,,4,,,,
2025-06-01,"Case New Holland,India",7500000411,,0,,,,
2023-04-01,"Case New Holland,India",7500000312,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000312,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000312,23.0,25,2.0,0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000312,30.0,32,2.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000312,48.0,0,-48.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000312,30.0,35,5.0,0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000312,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000312,50.0,30,-20.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000312,62.0,52,-10.0,-0.16129032258064516,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000312,60.0,32,-28.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000312,78.0,54,-24.0,-0.3076923076923077,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000312,65.0,84,19.0,0.2923076923076923,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000312,60.0,55,-5.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000312,70.0,46,-24.0,-0.34285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000312,70.0,37,-33.0,-0.4714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000312,88.0,60,-28.0,-0.3181818181818182,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000312,78.0,33,-45.0,-0.5769230769230769,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000312,50.0,41,-9.0,-0.18,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000312,61.0,42,-19.0,-0.3114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000312,70.0,51,-19.0,-0.2714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000312,65.0,61,-4.0,-0.06153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000312,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000312,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000312,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000312,,0,,,,
2025-05-01,"Case New Holland,India",7500000312,,0,,,,
2025-06-01,"Case New Holland,India",7500000312,,0,,,,
2023-04-01,"Case New Holland,India",7500000311,20.0,23,3.0,0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000311,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000311,23.0,25,2.0,0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000311,30.0,32,2.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000311,48.0,0,-48.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000311,30.0,35,5.0,0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000311,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000311,50.0,30,-20.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000311,62.0,52,-10.0,-0.16129032258064516,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000311,52.0,20,-32.0,-0.6153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000311,80.0,46,-34.0,-0.425,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000311,65.0,84,19.0,0.2923076923076923,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000311,60.0,55,-5.0,-0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000311,70.0,46,-24.0,-0.34285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000311,70.0,37,-33.0,-0.4714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000311,88.0,60,-28.0,-0.3181818181818182,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000311,70.0,33,-37.0,-0.5285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000311,50.0,41,-9.0,-0.18,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000311,61.0,42,-19.0,-0.3114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000311,70.0,51,-19.0,-0.2714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000311,65.0,61,-4.0,-0.06153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000311,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000311,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000311,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000311,,0,,,,
2025-05-01,"Case New Holland,India",7500000311,,0,,,,
2025-06-01,"Case New Holland,India",7500000311,,0,,,,
2023-04-01,"Case New Holland,India",7500000680,102.0,70,-32.0,-0.3137254901960784,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000680,112.0,115,3.0,0.026785714285714284,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000680,50.0,120,70.0,1.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000680,210.0,215,5.0,0.023809523809523808,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000680,156.0,60,-96.0,-0.6153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000680,200.0,120,-80.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000680,220.0,181,-39.0,-0.17727272727272728,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000680,186.0,52,-134.0,-0.7204301075268817,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000680,182.0,160,-22.0,-0.12087912087912088,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000680,66.0,80,14.0,0.21212121212121213,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000680,44.0,110,66.0,1.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000680,140.0,80,-60.0,-0.42857142857142855,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000680,300.0,340,40.0,0.13333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000680,184.0,190,6.0,0.03260869565217391,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000680,290.0,204,-86.0,-0.296551724137931,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000680,364.0,380,16.0,0.04395604395604396,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000680,200.0,200,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000680,100.0,100,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000680,152.0,155,3.0,0.019736842105263157,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000680,192.0,200,8.0,0.041666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000680,76.0,0,-76.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000680,50.0,200,150.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000680,200.0,115,-85.0,-0.425,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000680,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000680,,100,,,,
2025-05-01,"Case New Holland,India",7500000680,,160,,,,
2025-06-01,"Case New Holland,India",7500000680,,0,,,,
2023-04-01,"Case New Holland,India",7500000363,75.0,45,-30.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000363,48.0,32,-16.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000363,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000363,60.0,38,-22.0,-0.36666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000363,100.0,94,-6.0,-0.06,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000363,80.0,30,-50.0,-0.625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000363,120.0,88,-32.0,-0.26666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000363,152.0,106,-46.0,-0.3026315789473684,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000363,180.0,95,-85.0,-0.4722222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000363,153.0,40,-113.0,-0.738562091503268,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000363,209.0,110,-99.0,-0.47368421052631576,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000363,153.0,76,-77.0,-0.5032679738562091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000363,150.0,92,-58.0,-0.38666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000363,190.0,128,-62.0,-0.3263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000363,200.0,145,-55.0,-0.275,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000363,200.0,96,-104.0,-0.52,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000363,234.0,61,-173.0,-0.7393162393162394,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000363,110.0,85,-25.0,-0.22727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000363,122.0,147,25.0,0.20491803278688525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000363,150.0,76,-74.0,-0.49333333333333335,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000363,127.0,105,-22.0,-0.1732283464566929,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000363,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000363,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000363,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000363,,0,,,,
2025-05-01,"Case New Holland,India",7500000363,,0,,,,
2025-06-01,"Case New Holland,India",7500000363,,0,,,,
2023-04-01,"Case New Holland,India",7500000354,377.0,310,-67.0,-0.17771883289124668,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000354,227.0,170,-57.0,-0.2511013215859031,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000354,370.0,177,-193.0,-0.5216216216216216,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000354,449.0,308,-141.0,-0.31403118040089084,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000354,318.0,230,-88.0,-0.27672955974842767,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000354,400.0,270,-130.0,-0.325,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000354,400.0,223,-177.0,-0.4425,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000354,507.0,132,-375.0,-0.7396449704142012,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000354,400.0,204,-196.0,-0.49,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000354,254.0,185,-69.0,-0.27165354330708663,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000354,211.0,190,-21.0,-0.0995260663507109,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000354,278.0,225,-53.0,-0.1906474820143885,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000354,338.0,395,57.0,0.16863905325443787,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000354,403.0,165,-238.0,-0.5905707196029777,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000354,400.0,200,-200.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000354,442.0,721,279.0,0.6312217194570136,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000354,301.0,511,210.0,0.6976744186046512,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000354,150.0,251,101.0,0.6733333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000354,180.0,180,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000354,100.0,242,142.0,1.42,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000354,138.0,135,-3.0,-0.021739130434782608,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000354,350.0,447,97.0,0.27714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000354,300.0,683,383.0,1.2766666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000354,300.0,300,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000354,,195,,,,
2025-05-01,"Case New Holland,India",7500000354,,244,,,,
2025-06-01,"Case New Holland,India",7500000354,,165,,,,
2023-04-01,"Case New Holland,India",7500000542,714.0,530,-184.0,-0.25770308123249297,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000542,650.0,405,-245.0,-0.3769230769230769,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000542,700.0,507,-193.0,-0.2757142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000542,746.0,495,-251.0,-0.33646112600536193,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000542,606.0,339,-267.0,-0.4405940594059406,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000542,600.0,410,-190.0,-0.31666666666666665,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000542,400.0,517,117.0,0.2925,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000542,613.0,430,-183.0,-0.29853181076672103,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000542,450.0,434,-16.0,-0.035555555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000542,400.0,192,-208.0,-0.52,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000542,506.0,460,-46.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000542,400.0,251,-149.0,-0.3725,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000542,500.0,340,-160.0,-0.32,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000542,643.0,435,-208.0,-0.3234836702954899,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000542,600.0,539,-61.0,-0.10166666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000542,600.0,459,-141.0,-0.235,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000542,600.0,416,-184.0,-0.30666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000542,500.0,354,-146.0,-0.292,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000542,550.0,460,-90.0,-0.16363636363636364,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000542,500.0,305,-195.0,-0.39,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000542,619.0,414,-205.0,-0.33117932148626816,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000542,400.0,400,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000542,400.0,288,-112.0,-0.28,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000542,369.0,267,-102.0,-0.2764227642276423,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000542,,250,,,,
2025-05-01,"Case New Holland,India",7500000542,,279,,,,
2025-06-01,"Case New Holland,India",7500000542,,336,,,,
2023-04-01,"Case New Holland,India",7500000548,113.0,75,-38.0,-0.336283185840708,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000548,100.0,118,18.0,0.18,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000548,123.0,74,-49.0,-0.3983739837398374,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000548,212.0,140,-72.0,-0.33962264150943394,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000548,130.0,140,10.0,0.07692307692307693,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000548,120.0,167,47.0,0.39166666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000548,120.0,130,10.0,0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000548,90.0,140,50.0,0.5555555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000548,32.0,120,88.0,2.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000548,44.0,100,56.0,1.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000548,60.0,9,-51.0,-0.85,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000548,35.0,0,-35.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000548,88.0,100,12.0,0.13636363636363635,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000548,76.0,100,24.0,0.3157894736842105,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000548,60.0,40,-20.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000548,107.0,110,3.0,0.028037383177570093,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000548,0.0,17,17.0,17.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000548,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000548,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000548,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000548,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000548,54.0,0,-54.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000548,124.0,0,-124.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000548,50.0,0,-50.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000548,,96,,,,
2025-05-01,"Case New Holland,India",7500000548,,50,,,,
2025-06-01,"Case New Holland,India",7500000548,,0,,,,
2023-04-01,"Case New Holland,India",7500000362,42.0,48,6.0,0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000362,60.0,32,-28.0,-0.4666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000362,40.0,56,16.0,0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000362,29.0,25,-4.0,-0.13793103448275862,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000362,30.0,25,-5.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000362,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000362,30.0,17,-13.0,-0.43333333333333335,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000362,27.0,9,-18.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000362,41.0,35,-6.0,-0.14634146341463414,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000362,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000362,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000362,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000362,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000362,5.0,4,-1.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000362,12.0,12,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000362,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000362,0.0,5,5.0,5.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000362,0.0,5,5.0,5.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000362,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000362,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000362,0.0,4,4.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000362,52.0,4,-48.0,-0.9230769230769231,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000362,68.0,23,-45.0,-0.6617647058823529,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000362,55.0,1,-54.0,-0.9818181818181818,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000362,,29,,,,
2025-05-01,"Case New Holland,India",7500000362,,7,,,,
2025-06-01,"Case New Holland,India",7500000362,,18,,,,
2023-04-01,"Case New Holland,India",7500000350,100.0,62,-38.0,-0.38,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000350,60.0,54,-6.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000350,44.0,67,23.0,0.5227272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000350,100.0,90,-10.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000350,50.0,30,-20.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000350,80.0,68,-12.0,-0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000350,100.0,80,-20.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000350,78.0,30,-48.0,-0.6153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000350,100.0,36,-64.0,-0.64,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000350,98.0,52,-46.0,-0.46938775510204084,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000350,76.0,42,-34.0,-0.4473684210526316,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000350,56.0,13,-43.0,-0.7678571428571429,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000350,70.0,30,-40.0,-0.5714285714285714,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000350,100.0,17,-83.0,-0.83,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000350,160.0,147,-13.0,-0.08125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000350,89.0,42,-47.0,-0.5280898876404494,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000350,40.0,29,-11.0,-0.275,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000350,0.0,18,18.0,18.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000350,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000350,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000350,62.0,0,-62.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000350,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000350,100.0,38,-62.0,-0.62,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000350,100.0,40,-60.0,-0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000350,,60,,,,
2025-05-01,"Case New Holland,India",7500000350,,46,,,,
2025-06-01,"Case New Holland,India",7500000350,,60,,,,
2023-04-01,"Case New Holland,India",7500000469,113.0,83,-30.0,-0.26548672566371684,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000469,72.0,50,-22.0,-0.3055555555555556,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000469,90.0,90,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000469,90.0,30,-60.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000469,144.0,117,-27.0,-0.1875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000469,80.0,80,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000469,180.0,100,-80.0,-0.4444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000469,160.0,40,-120.0,-0.75,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000469,246.0,172,-74.0,-0.3008130081300813,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000469,200.0,148,-52.0,-0.26,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000469,200.0,129,-71.0,-0.355,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000469,189.0,91,-98.0,-0.5185185185185185,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000469,188.0,84,-104.0,-0.5531914893617021,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000469,200.0,153,-47.0,-0.235,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000469,150.0,100,-50.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000469,180.0,149,-31.0,-0.17222222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000469,111.0,120,9.0,0.08108108108108109,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000469,80.0,88,8.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000469,122.0,96,-26.0,-0.21311475409836064,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000469,130.0,20,-110.0,-0.8461538461538461,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000469,125.0,88,-37.0,-0.296,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000469,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000469,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000469,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000469,,0,,,,
2025-05-01,"Case New Holland,India",7500000469,,0,,,,
2025-06-01,"Case New Holland,India",7500000469,,0,,,,
2023-04-01,"Case New Holland,India",7500000845,98.0,83,-15.0,-0.15306122448979592,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000845,90.0,33,-57.0,-0.6333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000845,135.0,63,-72.0,-0.5333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000845,168.0,15,-153.0,-0.9107142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000845,129.0,147,18.0,0.13953488372093023,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000845,150.0,72,-78.0,-0.52,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000845,100.0,56,-44.0,-0.44,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000845,226.0,74,-152.0,-0.672566371681416,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000845,100.0,133,33.0,0.33,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000845,80.0,57,-23.0,-0.2875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000845,83.0,50,-33.0,-0.39759036144578314,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000845,107.0,66,-41.0,-0.38317757009345793,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000845,84.0,84,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000845,76.0,76,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000845,58.0,70,12.0,0.20689655172413793,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000845,75.0,80,5.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000845,30.0,32,2.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000845,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000845,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000845,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000845,49.0,49,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000845,54.0,55,1.0,0.018518518518518517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000845,70.0,58,-12.0,-0.17142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000845,60.0,40,-20.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000845,,49,,,,
2025-05-01,"Case New Holland,India",7500000845,,18,,,,
2025-06-01,"Case New Holland,India",7500000845,,80,,,,
2023-04-01,"Case New Holland,India",7500000342,42.0,30,-12.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000342,38.0,33,-5.0,-0.13157894736842105,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000342,32.0,30,-2.0,-0.0625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000342,29.0,29,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000342,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000342,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000342,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000342,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000342,44.0,30,-14.0,-0.3181818181818182,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000342,14.0,2,-12.0,-0.8571428571428571,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000342,12.0,20,8.0,0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000342,5.0,6,1.0,0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000342,7.0,7,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000342,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000342,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000342,20.0,23,3.0,0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000342,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000342,,0,,,,
2025-05-01,"Case New Holland,India",7500000342,,9,,,,
2025-06-01,"Case New Holland,India",7500000342,,0,,,,
2023-04-01,"Case New Holland,India",7500000344,30.0,31,1.0,0.03333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000344,32.0,23,-9.0,-0.28125,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000344,29.0,29,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000344,0.0,11,11.0,11.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000344,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000344,20.0,18,-2.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000344,22.0,50,28.0,1.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000344,14.0,35,21.0,1.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000344,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000344,5.0,10,5.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000344,2.0,4,2.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000344,11.0,12,1.0,0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000344,0.0,24,24.0,24.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000344,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000344,,0,,,,
2025-05-01,"Case New Holland,India",7500000344,,2,,,,
2025-06-01,"Case New Holland,India",7500000344,,0,,,,
2023-04-01,"Case New Holland,India",7500000361,42.0,43,1.0,0.023809523809523808,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000361,60.0,36,-24.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000361,40.0,46,6.0,0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000361,29.0,25,-4.0,-0.13793103448275862,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000361,20.0,25,5.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000361,30.0,33,3.0,0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000361,50.0,27,-23.0,-0.46,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000361,37.0,9,-28.0,-0.7567567567567568,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000361,14.0,34,20.0,1.4285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000361,5.0,1,-4.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000361,12.0,12,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000361,13.0,13,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000361,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000361,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000361,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000361,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000361,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000361,,13,,,,
2025-05-01,"Case New Holland,India",7500000361,,6,,,,
2025-06-01,"Case New Holland,India",7500000361,,18,,,,
2023-04-01,"Case New Holland,India",7500000323,48.0,32,-16.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000323,38.0,4,-34.0,-0.8947368421052632,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000323,32.0,20,-12.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000323,29.0,0,-29.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000323,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000323,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000323,20.0,60,40.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000323,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000323,14.0,50,36.0,2.5714285714285716,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000323,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000323,12.0,0,-12.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000323,25.0,25,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000323,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000323,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000323,,3,,,,
2025-05-01,"Case New Holland,India",7500000323,,12,,,,
2025-06-01,"Case New Holland,India",7500000323,,0,,,,
2023-04-01,"Case New Holland,India",7500000409,42.0,35,-7.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000409,38.0,20,-18.0,-0.47368421052631576,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000409,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000409,29.0,29,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000409,20.0,25,5.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000409,31.0,35,4.0,0.12903225806451613,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000409,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000409,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000409,14.0,15,1.0,0.07142857142857142,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000409,0.0,5,5.0,5.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000409,0.0,20,20.0,20.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000409,5.0,10,5.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000409,2.0,7,5.0,2.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000409,8.0,8,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000409,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000409,,0,,,,
2025-05-01,"Case New Holland,India",7500000409,,14,,,,
2025-06-01,"Case New Holland,India",7500000409,,0,,,,
2023-04-01,"Case New Holland,India",7500000410,42.0,35,-7.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000410,38.0,20,-18.0,-0.47368421052631576,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000410,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000410,29.0,29,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000410,20.0,25,5.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000410,31.0,35,4.0,0.12903225806451613,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000410,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000410,30.0,20,-10.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000410,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000410,14.0,5,-9.0,-0.6428571428571429,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000410,9.0,20,11.0,1.2222222222222223,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000410,5.0,10,5.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000410,7.0,7,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000410,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000410,30.0,4,-26.0,-0.8666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000410,25.0,0,-25.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000410,25.0,0,-25.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000410,,20,,,,
2025-05-01,"Case New Holland,India",7500000410,,14,,,,
2025-06-01,"Case New Holland,India",7500000410,,16,,,,
2023-04-01,"Case New Holland,India",7500000509,32.0,35,3.0,0.09375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000509,23.0,25,2.0,0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000509,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000509,27.0,30,3.0,0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000509,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000509,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000509,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000509,40.0,90,50.0,1.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000509,45.0,42,-3.0,-0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000509,50.0,74,24.0,0.48,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000509,44.0,100,56.0,1.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000509,27.0,27,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000509,36.0,0,-36.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000509,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000509,24.0,25,1.0,0.041666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000509,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000509,54.0,55,1.0,0.018518518518518517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000509,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000509,,2,,,,
2025-05-01,"Case New Holland,India",7500000509,,0,,,,
2025-06-01,"Case New Holland,India",7500000509,,0,,,,
2023-04-01,"Case New Holland,India",7500000510,32.0,35,3.0,0.09375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000510,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000510,27.0,27,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000510,20.0,30,10.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000510,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000510,60.0,50,-10.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000510,50.0,70,20.0,0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000510,45.0,37,-8.0,-0.17777777777777778,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000510,55.0,108,53.0,0.9636363636363636,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000510,100.0,100,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000510,27.0,3,-24.0,-0.8888888888888888,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000510,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000510,84.0,85,1.0,0.011904761904761904,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000510,23.0,25,2.0,0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000510,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000510,54.0,55,1.0,0.018518518518518517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000510,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000510,,8,,,,
2025-05-01,"Case New Holland,India",7500000510,,0,,,,
2025-06-01,"Case New Holland,India",7500000510,,0,,,,
2023-04-01,"Case New Holland,India",7500000338,58.0,20,-38.0,-0.6551724137931034,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000338,38.0,40,2.0,0.05263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000338,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000338,29.0,23,-6.0,-0.20689655172413793,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000338,40.0,0,-40.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000338,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000338,20.0,30,10.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000338,30.0,45,15.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000338,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000338,20.0,0,-20.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000338,20.0,30,10.0,0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000338,28.0,30,2.0,0.07142857142857142,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000338,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000338,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000338,,16,,,,
2025-05-01,"Case New Holland,India",7500000338,,14,,,,
2025-06-01,"Case New Holland,India",7500000338,,0,,,,
2023-04-01,"Case New Holland,India",7500000887,32.0,38,6.0,0.1875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000887,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000887,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000887,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000887,0.0,25,25.0,25.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000887,27.0,0,-27.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000887,0.0,30,30.0,30.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000887,30.0,40,10.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000887,14.0,30,16.0,1.1428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000887,0.0,20,20.0,20.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000887,0.0,7,7.0,7.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000887,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000887,,0,,,,
2025-05-01,"Case New Holland,India",7500000887,,0,,,,
2025-06-01,"Case New Holland,India",7500000887,,0,,,,
2023-04-01,"Case New Holland,India",7500000360,42.0,50,8.0,0.19047619047619047,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000360,38.0,40,2.0,0.05263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000360,32.0,20,-12.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000360,33.0,33,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000360,21.0,21,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000360,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000360,30.0,15,-15.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000360,45.0,30,-15.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000360,25.0,30,5.0,0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000360,0.0,32,32.0,32.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000360,0.0,6,6.0,6.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000360,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000360,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000360,11.0,7,-4.0,-0.36363636363636365,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000360,15.0,0,-15.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000360,32.0,0,-32.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000360,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000360,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000360,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000360,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000360,1.0,5,4.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000360,28.0,30,2.0,0.07142857142857142,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000360,17.0,7,-10.0,-0.5882352941176471,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000360,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000360,,21,,,,
2025-05-01,"Case New Holland,India",7500000360,,0,,,,
2025-06-01,"Case New Holland,India",7500000360,,52,,,,
2023-04-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000355,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000355,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000355,10.0,32,22.0,2.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000355,3.0,3,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000355,6.0,0,-6.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000355,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000355,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000355,2.0,5,3.0,1.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000355,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000355,,0,,,,
2025-05-01,"Case New Holland,India",7500000355,,7,,,,
2025-06-01,"Case New Holland,India",7500000355,,0,,,,
2023-04-01,"Case New Holland,India",7500000737,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000737,29.0,0,-29.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000737,19.0,0,-19.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000737,47.0,75,28.0,0.5957446808510638,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000737,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000737,24.0,0,-24.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000737,21.0,27,6.0,0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000737,55.0,0,-55.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000737,71.0,0,-71.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000737,86.0,0,-86.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000737,99.0,0,-99.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000737,99.0,100,1.0,0.010101010101010102,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000737,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000737,48.0,52,4.0,0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000737,75.0,0,-75.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000737,111.0,73,-38.0,-0.34234234234234234,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000737,32.0,0,-32.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000737,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000737,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000737,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000737,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000737,8.0,50,42.0,5.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000737,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000737,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000737,,0,,,,
2025-05-01,"Case New Holland,India",7500000737,,25,,,,
2025-06-01,"Case New Holland,India",7500000737,,25,,,,
2023-04-01,"Case New Holland,India",7500000701,52.0,28,-24.0,-0.46153846153846156,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000701,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000701,25.0,47,22.0,0.88,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000701,51.0,89,38.0,0.7450980392156863,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000701,24.0,40,16.0,0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000701,50.0,50,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000701,26.0,57,31.0,1.1923076923076923,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000701,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000701,90.0,20,-70.0,-0.7777777777777778,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000701,103.0,0,-103.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000701,129.0,103,-26.0,-0.20155038759689922,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000701,25.0,0,-25.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000701,49.0,14,-35.0,-0.7142857142857143,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000701,79.0,34,-45.0,-0.569620253164557,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000701,119.0,14,-105.0,-0.8823529411764706,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000701,147.0,54,-93.0,-0.6326530612244898,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000701,36.0,80,44.0,1.2222222222222223,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000701,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000701,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000701,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000701,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000701,15.0,0,-15.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000701,45.0,0,-45.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000701,67.0,27,-40.0,-0.5970149253731343,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000701,,79,,,,
2025-05-01,"Case New Holland,India",7500000701,,0,,,,
2025-06-01,"Case New Holland,India",7500000701,,0,,,,
2023-04-01,"Case New Holland,India",7500000492,38.0,40,2.0,0.05263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000492,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000492,23.0,23,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000492,24.0,20,-4.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000492,34.0,29,-5.0,-0.14705882352941177,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000492,62.0,70,8.0,0.12903225806451613,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000492,90.0,14,-76.0,-0.8444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000492,100.0,160,60.0,0.6,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000492,45.0,50,5.0,0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000492,44.0,50,6.0,0.13636363636363635,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000492,35.0,25,-10.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000492,41.0,44,3.0,0.07317073170731707,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000492,52.0,10,-42.0,-0.8076923076923077,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000492,72.0,75,3.0,0.041666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000492,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000492,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000492,,0,,,,
2025-05-01,"Case New Holland,India",7500000492,,0,,,,
2025-06-01,"Case New Holland,India",7500000492,,0,,,,
2023-04-01,"Case New Holland,India",7500000470,135.0,78,-57.0,-0.4222222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000470,72.0,48,-24.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000470,69.0,70,1.0,0.014492753623188406,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000470,90.0,96,6.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000470,192.0,205,13.0,0.06770833333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000470,80.0,92,12.0,0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000470,93.0,170,77.0,0.8279569892473119,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000470,400.0,83,-317.0,-0.7925,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000470,500.0,336,-164.0,-0.328,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000470,314.0,87,-227.0,-0.7229299363057324,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000470,371.0,100,-271.0,-0.7304582210242587,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000470,334.0,39,-295.0,-0.8832335329341318,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000470,90.0,39,-51.0,-0.5666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000470,147.0,88,-59.0,-0.4013605442176871,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000470,161.0,212,51.0,0.3167701863354037,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000470,100.0,105,5.0,0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000470,100.0,101,1.0,0.01,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000470,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000470,122.0,84,-38.0,-0.3114754098360656,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000470,126.0,42,-84.0,-0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000470,65.0,69,4.0,0.06153846153846154,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000470,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000470,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000470,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000470,,0,,,,
2025-05-01,"Case New Holland,India",7500000470,,0,,,,
2025-06-01,"Case New Holland,India",7500000470,,0,,,,
2023-04-01,"Case New Holland,India",7500000547,0.0,6,6.0,6.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000547,0.0,127,127.0,127.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000547,19.0,0,-19.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000547,21.0,0,-21.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000547,43.0,56,13.0,0.3023255813953488,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000547,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000547,75.0,0,-75.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000547,88.0,31,-57.0,-0.6477272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000547,57.0,65,8.0,0.14035087719298245,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000547,0.0,15,15.0,15.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000547,0.0,23,23.0,23.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000547,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000547,,0,,,,
2025-05-01,"Case New Holland,India",7500000547,,10,,,,
2025-06-01,"Case New Holland,India",7500000547,,0,,,,
2023-04-01,"Case New Holland,India",7500000551,443.0,395,-48.0,-0.10835214446952596,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000551,260.0,117,-143.0,-0.55,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000551,370.0,294,-76.0,-0.20540540540540542,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000551,449.0,497,48.0,0.10690423162583519,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000551,318.0,295,-23.0,-0.07232704402515723,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000551,250.0,240,-10.0,-0.04,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000551,200.0,230,30.0,0.15,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000551,200.0,138,-62.0,-0.31,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000551,200.0,201,1.0,0.005,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000551,72.0,30,-42.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000551,162.0,18,-144.0,-0.8888888888888888,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000551,168.0,12,-156.0,-0.9285714285714286,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000551,290.0,179,-111.0,-0.38275862068965516,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000551,370.0,90,-280.0,-0.7567567567567568,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000551,500.0,327,-173.0,-0.346,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000551,380.0,276,-104.0,-0.2736842105263158,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000551,294.0,170,-124.0,-0.4217687074829932,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000551,200.0,254,54.0,0.27,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000551,200.0,187,-13.0,-0.065,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000551,100.0,80,-20.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000551,110.0,106,-4.0,-0.03636363636363636,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000551,250.0,205,-45.0,-0.18,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000551,300.0,202,-98.0,-0.32666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000551,300.0,146,-154.0,-0.5133333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000551,,67,,,,
2025-05-01,"Case New Holland,India",7500000551,,231,,,,
2025-06-01,"Case New Holland,India",7500000551,,286,,,,
2023-04-01,"Case New Holland,India",7500000337,58.0,46,-12.0,-0.20689655172413793,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000337,38.0,18,-20.0,-0.5263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000337,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000337,29.0,0,-29.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000337,40.0,30,-10.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000337,30.0,60,30.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000337,20.0,15,-5.0,-0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000337,35.0,30,-5.0,-0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000337,14.0,60,46.0,3.2857142857142856,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000337,0.0,8,8.0,8.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000337,0.0,9,9.0,9.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000337,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000337,,0,,,,
2025-05-01,"Case New Holland,India",7500000337,,0,,,,
2025-06-01,"Case New Holland,India",7500000337,,1,,,,
2023-04-01,"Case New Holland,India",7500000366,58.0,58,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000366,38.0,32,-6.0,-0.15789473684210525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000366,32.0,20,-12.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000366,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000366,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000366,20.0,45,25.0,1.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000366,33.0,44,11.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000366,14.0,37,23.0,1.6428571428571428,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000366,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000366,0.0,13,13.0,13.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000366,0.0,2,2.0,2.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000366,,9,,,,
2025-05-01,"Case New Holland,India",7500000366,,30,,,,
2025-06-01,"Case New Holland,India",7500000366,,0,,,,
2023-04-01,"Case New Holland,India",7500000728,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000728,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000728,16.0,100,84.0,5.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000728,0.0,80,80.0,80.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000728,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000728,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000728,110.0,110,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000728,90.0,80,-10.0,-0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000728,30.0,40,10.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000728,22.0,30,8.0,0.36363636363636365,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000728,22.0,180,158.0,7.181818181818182,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000728,70.0,330,260.0,3.7142857142857144,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000728,114.0,210,96.0,0.8421052631578947,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000728,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000728,0.0,200,200.0,200.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000728,0.0,110,110.0,110.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000728,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000728,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000728,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000728,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000728,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000728,0.0,200,200.0,200.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000728,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000728,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000728,,50,,,,
2025-05-01,"Case New Holland,India",7500000728,,0,,,,
2025-06-01,"Case New Holland,India",7500000728,,0,,,,
2023-04-01,"Case New Holland,India",7500000869,857.0,650,-207.0,-0.24154025670945156,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000869,504.0,485,-19.0,-0.037698412698412696,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000869,529.0,550,21.0,0.03969754253308128,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000869,600.0,400,-200.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000869,808.0,400,-408.0,-0.504950495049505,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000869,500.0,500,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000869,454.0,500,46.0,0.1013215859030837,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000869,600.0,400,-200.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000869,500.0,300,-200.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000869,557.0,388,-169.0,-0.30341113105924594,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000869,557.0,350,-207.0,-0.37163375224416517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000869,594.0,500,-94.0,-0.15824915824915825,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000869,350.0,400,50.0,0.14285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000869,500.0,90,-410.0,-0.82,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000869,732.0,325,-407.0,-0.5560109289617486,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000869,885.0,650,-235.0,-0.2655367231638418,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000869,800.0,280,-520.0,-0.65,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000869,600.0,577,-23.0,-0.03833333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000869,516.0,239,-277.0,-0.5368217054263565,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000869,415.0,500,85.0,0.20481927710843373,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000869,455.0,455,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000869,350.0,355,5.0,0.014285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000869,400.0,385,-15.0,-0.0375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000869,232.0,225,-7.0,-0.03017241379310345,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000869,,300,,,,
2025-05-01,"Case New Holland,India",7500000869,,373,,,,
2025-06-01,"Case New Holland,India",7500000869,,400,,,,
2023-04-01,"Case New Holland,India",7500000870,857.0,550,-307.0,-0.35822637106184363,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000870,504.0,485,-19.0,-0.037698412698412696,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000870,529.0,550,21.0,0.03969754253308128,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000870,600.0,400,-200.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000870,808.0,305,-503.0,-0.6225247524752475,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000870,499.0,500,1.0,0.002004008016032064,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000870,454.0,500,46.0,0.1013215859030837,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000870,600.0,400,-200.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000870,500.0,300,-200.0,-0.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000870,557.0,388,-169.0,-0.30341113105924594,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000870,557.0,350,-207.0,-0.37163375224416517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000870,594.0,500,-94.0,-0.15824915824915825,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000870,400.0,400,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000870,550.0,90,-460.0,-0.8363636363636363,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000870,782.0,325,-457.0,-0.5843989769820972,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000870,935.0,650,-285.0,-0.3048128342245989,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000870,800.0,300,-500.0,-0.625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000870,600.0,575,-25.0,-0.041666666666666664,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000870,516.0,250,-266.0,-0.5155038759689923,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000870,500.0,500,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000870,550.0,455,-95.0,-0.17272727272727273,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000870,350.0,355,5.0,0.014285714285714285,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000870,400.0,385,-15.0,-0.0375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000870,232.0,225,-7.0,-0.03017241379310345,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000870,,300,,,,
2025-05-01,"Case New Holland,India",7500000870,,373,,,,
2025-06-01,"Case New Holland,India",7500000870,,400,,,,
2023-04-01,"Case New Holland,India",7500000682,100.0,70,-30.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000682,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000682,16.0,90,74.0,4.625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000682,70.0,93,23.0,0.32857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000682,50.0,40,-10.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000682,100.0,50,-50.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000682,110.0,118,8.0,0.07272727272727272,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000682,137.0,40,-97.0,-0.708029197080292,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000682,120.0,100,-20.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000682,42.0,51,9.0,0.21428571428571427,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000682,22.0,35,13.0,0.5909090909090909,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000682,77.0,100,23.0,0.2987012987012987,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000682,114.0,130,16.0,0.14035087719298245,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000682,92.0,130,38.0,0.41304347826086957,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000682,110.0,105,-5.0,-0.045454545454545456,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000682,120.0,120,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000682,60.0,65,5.0,0.08333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000682,0.0,50,50.0,50.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000682,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000682,0.0,50,50.0,50.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000682,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000682,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000682,0.0,100,100.0,100.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000682,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000682,,50,,,,
2025-05-01,"Case New Holland,India",7500000682,,0,,,,
2025-06-01,"Case New Holland,India",7500000682,,50,,,,
2023-04-01,"Case New Holland,India",7500000503,20.0,25,5.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000503,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000503,24.0,12,-12.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000503,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000503,62.0,92,30.0,0.4838709677419355,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000503,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000503,41.0,0,-41.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000503,88.0,100,12.0,0.13636363636363635,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000503,80.0,14,-66.0,-0.825,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000503,136.0,118,-18.0,-0.1323529411764706,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000503,41.0,42,1.0,0.024390243902439025,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000503,52.0,50,-2.0,-0.038461538461538464,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000503,45.0,45,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000503,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000503,,0,,,,
2025-05-01,"Case New Holland,India",7500000503,,0,,,,
2025-06-01,"Case New Holland,India",7500000503,,0,,,,
2023-04-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000341,32.0,32,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000341,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000341,0.0,25,25.0,25.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000341,30.0,39,9.0,0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000341,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000341,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000341,15.0,0,-15.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000341,15.0,0,-15.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000341,15.0,50,35.0,2.3333333333333335,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000341,0.0,24,24.0,24.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000341,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000341,,0,,,,
2025-05-01,"Case New Holland,India",7500000341,,13,,,,
2025-06-01,"Case New Holland,India",7500000341,,0,,,,
2023-04-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000678,0.0,13,13.0,13.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000678,0.0,30,30.0,30.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000678,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000678,0.0,83,83.0,83.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000678,0.0,39,39.0,39.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000678,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000678,,0,,,,
2025-05-01,"Case New Holland,India",7500000678,,0,,,,
2025-06-01,"Case New Holland,India",7500000678,,0,,,,
2023-04-01,"Case New Holland,India",7500000367,2646.0,1380,-1266.0,-0.47845804988662133,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000367,2500.0,1780,-720.0,-0.288,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000367,1868.0,1700,-168.0,-0.08993576017130621,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000367,2000.0,2050,50.0,0.025,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000367,2000.0,700,-1300.0,-0.65,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000367,2000.0,2100,100.0,0.05,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000367,1736.0,1770,34.0,0.019585253456221197,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000367,1700.0,1190,-510.0,-0.3,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000367,2000.0,1450,-550.0,-0.275,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000367,1778.0,2050,272.0,0.1529808773903262,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000367,2000.0,1190,-810.0,-0.405,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000367,2116.0,1045,-1071.0,-0.5061436672967864,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000367,2000.0,2010,10.0,0.005,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000367,1936.0,1180,-756.0,-0.390495867768595,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000367,2102.0,1600,-502.0,-0.23882017126546146,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000367,2652.0,2300,-352.0,-0.13273001508295626,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000367,2500.0,2110,-390.0,-0.156,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000367,2026.0,1785,-241.0,-0.11895360315893386,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000367,1755.0,1770,15.0,0.008547008547008548,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000367,2000.0,1800,-200.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000367,1774.0,1590,-184.0,-0.10372040586245772,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000367,1300.0,1330,30.0,0.023076923076923078,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000367,1300.0,1400,100.0,0.07692307692307693,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000367,1000.0,892,-108.0,-0.108,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000367,,1150,,,,
2025-05-01,"Case New Holland,India",7500000367,,1255,,,,
2025-06-01,"Case New Holland,India",7500000367,,2050,,,,
2023-04-01,"Case New Holland,India",7500000465,270.0,215,-55.0,-0.2037037037037037,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000465,222.0,240,18.0,0.08108108108108109,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000465,246.0,80,-166.0,-0.6747967479674797,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000465,300.0,300,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000465,348.0,200,-148.0,-0.42528735632183906,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000465,250.0,320,70.0,0.28,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000465,222.0,225,3.0,0.013513513513513514,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000465,240.0,200,-40.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000465,100.0,120,20.0,0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000465,88.0,260,172.0,1.9545454545454546,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000465,120.0,50,-70.0,-0.5833333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000465,204.0,80,-124.0,-0.6078431372549019,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000465,106.0,110,4.0,0.03773584905660377,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000465,152.0,150,-2.0,-0.013157894736842105,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000465,176.0,180,4.0,0.022727272727272728,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000465,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000465,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000465,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000465,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000465,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000465,98.0,100,2.0,0.02040816326530612,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000465,108.0,40,-68.0,-0.6296296296296297,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000465,208.0,160,-48.0,-0.23076923076923078,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000465,203.0,30,-173.0,-0.8522167487684729,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000465,,190,,,,
2025-05-01,"Case New Holland,India",7500000465,,140,,,,
2025-06-01,"Case New Holland,India",7500000465,,110,,,,
2023-04-01,"Case New Holland,India",7500000347,466.0,300,-166.0,-0.3562231759656652,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000347,196.0,230,34.0,0.17346938775510204,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000347,405.0,290,-115.0,-0.2839506172839506,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000347,633.0,450,-183.0,-0.2890995260663507,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000347,730.0,440,-290.0,-0.3972602739726027,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000347,460.0,460,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000347,412.0,450,38.0,0.09223300970873786,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000347,612.0,400,-212.0,-0.3464052287581699,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000347,600.0,400,-200.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000347,557.0,600,43.0,0.07719928186714542,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000347,600.0,371,-229.0,-0.38166666666666665,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000347,563.0,438,-125.0,-0.22202486678507993,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000347,300.0,300,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000347,468.0,200,-268.0,-0.5726495726495726,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000347,669.0,180,-489.0,-0.7309417040358744,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000347,900.0,538,-362.0,-0.4022222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000347,775.0,530,-245.0,-0.3161290322580645,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000347,470.0,376,-94.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000347,435.0,256,-179.0,-0.4114942528735632,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000347,415.0,420,5.0,0.012048192771084338,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000347,438.0,470,32.0,0.0730593607305936,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000347,281.0,300,19.0,0.06761565836298933,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000347,300.0,300,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000347,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000347,,300,,,,
2025-05-01,"Case New Holland,India",7500000347,,177,,,,
2025-06-01,"Case New Holland,India",7500000347,,510,,,,
2023-04-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000356,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000356,8.0,5,-3.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000356,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000356,5.0,37,32.0,6.4,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000356,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000356,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000356,,0,,,,
2025-05-01,"Case New Holland,India",7500000356,,5,,,,
2025-06-01,"Case New Holland,India",7500000356,,0,,,,
2023-04-01,"Case New Holland,India",7500000821,72.0,80,8.0,0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000821,55.0,65,10.0,0.18181818181818182,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000821,59.0,100,41.0,0.6949152542372882,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000821,122.0,100,-22.0,-0.18032786885245902,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000821,52.0,0,-52.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000821,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000821,45.0,100,55.0,1.2222222222222223,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000821,35.0,50,15.0,0.42857142857142855,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000821,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000821,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000821,10.0,0,-10.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000821,10.0,100,90.0,9.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000821,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000821,0.0,22,22.0,22.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000821,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000821,,0,,,,
2025-05-01,"Case New Holland,India",7500000821,,15,,,,
2025-06-01,"Case New Holland,India",7500000821,,0,,,,
2023-04-01,"Case New Holland,India",7500000874,53.0,55,2.0,0.03773584905660377,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000874,55.0,48,-7.0,-0.12727272727272726,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000874,56.0,38,-18.0,-0.32142857142857145,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000874,90.0,110,20.0,0.2222222222222222,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000874,88.0,0,-88.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000874,70.0,70,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000874,60.0,40,-20.0,-0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000874,60.0,71,11.0,0.18333333333333332,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000874,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000874,40.0,80,40.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000874,80.0,122,42.0,0.525,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000874,0.0,50,50.0,50.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000874,37.0,40,3.0,0.08108108108108109,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000874,60.0,50,-10.0,-0.16666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000874,65.0,65,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000874,38.0,40,2.0,0.05263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000874,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000874,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000874,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000874,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000874,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000874,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000874,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000874,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000874,,0,,,,
2025-05-01,"Case New Holland,India",7500000874,,2,,,,
2025-06-01,"Case New Holland,India",7500000874,,0,,,,
2023-04-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500001923,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500001923,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500001923,12.0,20,8.0,0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500001923,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500001923,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500001923,0.0,17,17.0,17.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500001923,,0,,,,
2025-05-01,"Case New Holland,India",7500001923,,5,,,,
2025-06-01,"Case New Holland,India",7500001923,,0,,,,
2023-04-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000908,4.0,0,-4.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000908,8.0,5,-3.0,-0.375,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000908,10.0,5,-5.0,-0.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000908,5.0,0,-5.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000908,5.0,20,15.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000908,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000908,0.0,38,38.0,38.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000908,,0,,,,
2025-05-01,"Case New Holland,India",7500000908,,3,,,,
2025-06-01,"Case New Holland,India",7500000908,,0,,,,
2023-04-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000500,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000500,10.0,10,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000500,24.0,0,-24.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000500,30.0,30,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000500,62.0,124,62.0,1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000500,90.0,90,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000500,41.0,0,-41.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000500,88.0,100,12.0,0.13636363636363635,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000500,44.0,200,156.0,3.5454545454545454,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000500,53.0,40,-13.0,-0.24528301886792453,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000500,37.0,0,-37.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000500,37.0,0,-37.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000500,0.0,14,14.0,14.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000500,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000500,,0,,,,
2025-05-01,"Case New Holland,India",7500000500,,10,,,,
2025-06-01,"Case New Holland,India",7500000500,,0,,,,
2023-04-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000497,40.0,0,-40.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000497,90.0,0,-90.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000497,100.0,100,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000497,248.0,250,2.0,0.008064516129032258,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000497,200.0,200,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000497,160.0,0,-160.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000497,348.0,400,52.0,0.14942528735632185,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000497,350.0,0,-350.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000497,596.0,360,-236.0,-0.3959731543624161,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000497,200.0,200,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000497,60.0,60,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000497,208.0,220,12.0,0.057692307692307696,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000497,150.0,150,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000497,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000497,,0,,,,
2025-05-01,"Case New Holland,India",7500000497,,0,,,,
2025-06-01,"Case New Holland,India",7500000497,,0,,,,
2023-04-01,"Case New Holland,India",7500000502,151.0,80,-71.0,-0.47019867549668876,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000502,92.0,100,8.0,0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000502,40.0,0,-40.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000502,90.0,50,-40.0,-0.4444444444444444,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000502,200.0,180,-20.0,-0.1,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000502,108.0,120,12.0,0.1111111111111111,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000502,248.0,250,2.0,0.008064516129032258,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000502,250.0,0,-250.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000502,400.0,258,-142.0,-0.355,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000502,330.0,400,70.0,0.21212121212121213,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000502,400.0,90,-310.0,-0.775,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000502,454.0,446,-8.0,-0.01762114537444934,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000502,0.0,3,3.0,3.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000502,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000502,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000502,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000502,164.0,107,-57.0,-0.3475609756097561,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000502,60.0,59,-1.0,-0.016666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000502,227.0,54,-173.0,-0.762114537444934,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000502,249.0,241,-8.0,-0.0321285140562249,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000502,276.0,38,-238.0,-0.8623188405797102,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000502,15.0,27,12.0,0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000502,15.0,16,1.0,0.06666666666666667,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000502,14.0,0,-14.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000502,,7,,,,
2025-05-01,"Case New Holland,India",7500000502,,10,,,,
2025-06-01,"Case New Holland,India",7500000502,,55,,,,
2023-04-01,"Case New Holland,India",7500000681,0.0,36,36.0,36.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000681,0.0,84,84.0,84.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000681,16.0,80,64.0,4.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000681,0.0,20,20.0,20.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000681,50.0,40,-10.0,-0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000681,100.0,15,-85.0,-0.85,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000681,110.0,100,-10.0,-0.09090909090909091,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000681,125.0,0,-125.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000681,140.0,100,-40.0,-0.2857142857142857,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000681,62.0,65,3.0,0.04838709677419355,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000681,22.0,50,28.0,1.2727272727272727,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000681,82.0,50,-32.0,-0.3902439024390244,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000681,146.0,110,-36.0,-0.2465753424657534,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000681,128.0,90,-38.0,-0.296875,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000681,186.0,190,4.0,0.021505376344086023,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000681,120.0,160,40.0,0.3333333333333333,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000681,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000681,120.0,0,-120.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000681,196.0,170,-26.0,-0.1326530612244898,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000681,0.0,50,50.0,50.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000681,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000681,8.0,0,-8.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000681,100.0,185,85.0,0.85,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000681,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000681,,100,,,,
2025-05-01,"Case New Holland,India",7500000681,,100,,,,
2025-06-01,"Case New Holland,India",7500000681,,0,,,,
2023-04-01,"Case New Holland,India",7500000508,58.0,50,-8.0,-0.13793103448275862,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000508,38.0,30,-8.0,-0.21052631578947367,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000508,32.0,52,20.0,0.625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000508,19.0,20,1.0,0.05263157894736842,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000508,0.0,50,50.0,50.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000508,30.0,50,20.0,0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000508,20.0,20,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000508,30.0,0,-30.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000508,44.0,60,16.0,0.36363636363636365,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000508,0.0,70,70.0,70.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000508,0.0,24,24.0,24.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000508,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000508,,50,,,,
2025-05-01,"Case New Holland,India",7500000508,,7,,,,
2025-06-01,"Case New Holland,India",7500000508,,0,,,,
2023-04-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000402,0.0,60,60.0,60.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000402,54.0,50,-4.0,-0.07407407407407407,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000402,0.0,40,40.0,40.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000402,4.0,4,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000402,100.0,100,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000402,50.0,90,40.0,0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000402,0.0,10,10.0,10.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000402,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000402,,0,,,,
2025-05-01,"Case New Holland,India",7500000402,,10,,,,
2025-06-01,"Case New Holland,India",7500000402,,0,,,,
2023-04-01,"Case New Holland,India",7500000513,151.0,80,-71.0,-0.47019867549668876,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000513,92.0,100,8.0,0.08695652173913043,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000513,40.0,40,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000513,99.0,100,1.0,0.010101010101010102,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000513,100.0,120,20.0,0.2,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000513,140.0,0,-140.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000513,256.0,400,144.0,0.5625,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000513,300.0,60,-240.0,-0.8,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000513,400.0,330,-70.0,-0.175,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000513,258.0,0,-258.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000513,434.0,409,-25.0,-0.0576036866359447,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000513,200.0,0,-200.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000513,150.0,150,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000513,212.0,130,-82.0,-0.3867924528301887,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000513,170.0,110,-60.0,-0.35294117647058826,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000513,148.0,0,-148.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000513,312.0,312,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000513,4.0,5,1.0,0.25,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000513,211.0,20,-191.0,-0.9052132701421801,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000513,275.0,100,-175.0,-0.6363636363636364,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000513,110.0,136,26.0,0.23636363636363636,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000513,4.0,34,30.0,7.5,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000513,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000513,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000513,,0,,,,
2025-05-01,"Case New Holland,India",7500000513,,2,,,,
2025-06-01,"Case New Holland,India",7500000513,,0,,,,
2023-04-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000401,16.0,16,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000401,18.0,30,12.0,0.6666666666666666,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000401,34.0,203,169.0,4.970588235294118,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000401,0.0,200,200.0,200.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000401,0.0,55,55.0,55.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000401,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000401,0.0,36,36.0,36.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000401,200.0,0,-200.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000401,200.0,200,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000401,,0,,,,
2025-05-01,"Case New Holland,India",7500000401,,0,,,,
2025-06-01,"Case New Holland,India",7500000401,,0,,,,
2023-04-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-05-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-06-01,"Case New Holland,India",7500000873,60.0,0,-60.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-07-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-08-01,"Case New Holland,India",7500000873,156.0,0,-156.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-09-01,"Case New Holland,India",7500000873,200.0,200,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-10-01,"Case New Holland,India",7500000873,396.0,0,-396.0,-1.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-11-01,"Case New Holland,India",7500000873,996.0,210,-786.0,-0.7891566265060241,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2023-12-01,"Case New Holland,India",7500000873,1000.0,590,-410.0,-0.41,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-01-01,"Case New Holland,India",7500000873,692.0,900,208.0,0.30057803468208094,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-02-01,"Case New Holland,India",7500000873,356.0,316,-40.0,-0.11235955056179775,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-03-01,"Case New Holland,India",7500000873,658.0,690,32.0,0.0486322188449848,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-04-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-05-01,"Case New Holland,India",7500000873,408.0,17,-391.0,-0.9583333333333334,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-06-01,"Case New Holland,India",7500000873,535.0,800,265.0,0.4953271028037383,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-07-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-08-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-09-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-10-01,"Case New Holland,India",7500000873,324.0,330,6.0,0.018518518518518517,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-11-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2024-12-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-01-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-02-01,"Case New Holland,India",7500000873,0.0,0,0.0,0.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-03-01,"Case New Holland,India",7500000873,0.0,143,143.0,143.0,"Construction,landscaping and Utility",Common parts of cabin used in india and gulf countries
2025-04-01,"Case New Holland,India",7500000873,,0,,,,
2025-05-01,"Case New Holland,India",7500000873,,25,,,,
2025-06-01,"Case New Holland,India",7500000873,,0,,,,
"""
holiday_csv = """Year,Month,Holiday Month Factor
2025,10,0.8
2026,11,0.8
"""

# Load embedded data
df = pd.read_csv(io.StringIO(csv_data), parse_dates=["Month"])
holiday_df = pd.read_csv(io.StringIO(holiday_csv))

# --- Data Preparation ---
df['Fiscal_Year'] = df['Month'].apply(lambda d: f"{d.year}-{d.year+1}" if d.month >= 4 else f"{d.year-1}-{d.year}")
df['Month_Num'] = df['Month'].dt.month

# --- Inflation & Tariff Factors ---
inflation_rate = 0.03
tariff_factor = 1.02

# --- CAGR Calculation ---
annual_totals = df.groupby(['Part No','Fiscal_Year'])['Actual Lifting Qty'].sum().unstack(fill_value=0)
def compute_cagr(start, end):
    return ((end / start)**(1/1) - 1) if start > 0 else 0
cagr_df = pd.DataFrame(index=annual_totals.index)
cagr_df['CAGR'] = [min(compute_cagr(annual_totals.loc[idx,'2023-2024'], annual_totals.loc[idx,'2024-2025']), 1.5)
                   for idx in annual_totals.index]

# --- Absolute Parts ---
last_date = df['Month'].max()
recent_8 = df[df['Month'] >= (last_date - pd.DateOffset(months=8))]
absolute_parts = recent_8.groupby('Part No')['Actual Lifting Qty'].sum()
absolute_parts = absolute_parts[absolute_parts == 0].index.tolist()

# --- Monthly Averages ---
monthly_avg = df[df['Fiscal_Year']=='2024-2025'].groupby(['Part No','Month_Num'])['Actual Lifting Qty'].mean()
part_segments = df[['Part No','Final product uasage','Supplying country']].drop_duplicates()

# --- Holiday Calendar Function ---
holiday_factors = dict(zip(holiday_df['Year'].astype(str) + "-" + holiday_df['Month'].astype(str).str.zfill(2), holiday_df['Holiday Month Factor']))
def holiday_adjustment(date):
    key = f"{date.year}-{str(date.month).zfill(2)}"
    return holiday_factors.get(key,1.0)

# --- Backlog Logic ---
df['Backlog'] = (df['Firm Schedule Qty'] - df['Actual Lifting Qty']).apply(lambda x: x if x>0 else 0)
backlog_uplift = {}
for _, row in df.iterrows():
    if row['Backlog']>0:
        m1=row['Month']+relativedelta(months=1)
        m2=row['Month']+relativedelta(months=2)
        backlog_uplift[(row['Part No'],m1)] = backlog_uplift.get((row['Part No'],m1),0)+(row['Backlog']*0.6)
        backlog_uplift[(row['Part No'],m2)] = backlog_uplift.get((row['Part No'],m2),0)+(row['Backlog']*0.4)

# --- Forecast Logic ---
forecast_months=pd.date_range(start='2025-04-01',end='2027-03-01',freq='MS')
forecast_data=[]
volatility_scores={}

for part_no in df['Part No'].unique():
    cagr=cagr_df.loc[part_no]['CAGR'] if part_no in cagr_df.index else 0
    hist= df[df['Part No']==part_no]['Actual Lifting Qty']
    volatility_scores[part_no]=hist.pct_change().abs().mean()*100

    for m in forecast_months:
        years_since=(m.year-2025)+((m.month-4)/12)
        base_qty=monthly_avg.get((part_no,m.month),0)
        forecast_val=base_qty*((1+cagr)**years_since)
        forecast_val*= (1+inflation_rate) * tariff_factor
        forecast_val*= holiday_adjustment(m)
        forecast_val+= backlog_uplift.get((part_no,m),0)

        if part_no in absolute_parts: forecast_val=0
        if part_no==7500000831 and m>=pd.to_datetime('2025-07-01'): forecast_val=0

        forecast_data.append({
            'Part No':part_no,
            'Month':m,
            'Final product uasage':part_segments[part_segments['Part No']==part_no]['Final product uasage'].values[0],
            'Supplying country':part_segments[part_segments['Part No']==part_no]['Supplying country'].values[0],
            'Forecasted Qty':round(forecast_val),
            'Volatility Score (%)':round(volatility_scores[part_no],2)
        })

forecast_df=pd.DataFrame(forecast_data)

# --- Streamlit UI ---
tab1,tab2,tab3=st.tabs(["Single Part Forecast","All Parts Forecast","Download Forecast"])

with tab1:
    part_list=sorted(forecast_df['Part No'].unique())
    selected_part=st.selectbox("Select Part No:",part_list)
    part_data=forecast_df[forecast_df['Part No']==selected_part]
    st.write(f"### Forecast for Part: {selected_part}")
    st.dataframe(part_data)

    fig,ax=plt.subplots()
    hist_data=df[df['Part No']==selected_part]
    ax.plot(hist_data['Month'],hist_data['Actual Lifting Qty'],label="Historical Actual")
    ax.plot(part_data['Month'],part_data['Forecasted Qty'],'--',label="Forecasted")
    ax.legend(); ax.set_xlabel("Month"); ax.set_ylabel("Quantity")
    st.pyplot(fig)

with tab2:
    st.write("### Forecast (All Parts with Segmentation & Confidence Scores)")
    st.dataframe(forecast_df)

with tab3:
    st.download_button("📥 Download Full Forecast",
                       data=forecast_df.to_csv(index=False),
                       file_name="Embedded_24_Month_Forecast.csv",
                       mime="text/csv")
