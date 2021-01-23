#!/usr/bin/env R

library(dplyr)
library(tidyverse)
library(ggplot2)
indir="report"
csvfiles <- list.files(path=indir,pattern = "*.csv",full.names=TRUE)
tbl <- csvfiles %>% map_df(~read_csv(.,col_types="icccccdccc")) %>% filter(AwardAmount > 0)
BIO <- tbl %>% filter(Directorate == "Direct For Biological Sciences") %>% filter(AwardAmount < 5e6)

hist(BIO$AwardAmount,100)
BIO_Small <- tbl %>% filter(Directorate == "Direct For Biological Sciences") %>% filter(AwardAmount < 5e5)
hist(BIO_Small$AwardAmount,100)

plot(BIO$Year,BIO$AwardAmount)

