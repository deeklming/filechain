package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"./blake2b"
)

func main() {
	starttime := time.Now()
	println("\n\t\t\t!!!HashFileChain!!!\n")
	var optslct string
	var pathslct string
	args := os.Args
	switch len(args) { //args check
	case 1:
		helpcheck("<Args check> No option! [FileChain Program] [Option] [Just one folder Path to hash]")
	case 2:
		if args[1] == "help" {
			println("help)\n[FileChain Program] [Option] [Just one folder Path to hash]")
			println("[Option]\n\tnew: 현제 폴더 새로운 해시 생성\n\tupdate: 해시 업데이트")
			println("\tverify: 검증\n\thelp: 사용법\n")
			return
		} else if args[1] == "new" || args[1] == "update" || args[1] == "verify" {
			println("<args check> More Path [FileChain Program] [Option] [Just one folder Path to hash]\n")
			return
		} else {
			helpcheck("<args check> No option! [FileChain Program] [Option] [Just one folder Path to hash]")
		}
	case 3:
		optslct = args[1]
		pathslct = args[2]
		switch optslct { //option check
		case "new":
		case "update":
		case "verify":
		case "help":
			helpcheck("help doesn't need a path.")
		default:
			helpcheck("Plz check option")
		}
		filepath, err := os.Open(pathslct) //path check
		defer filepath.Close()
		errcheck(err, "<path check> Can't open folder")
		fpath, err := filepath.Stat()
		errcheck(err, "<path check> Can't read folder stat")
		if fpath.IsDir() {
			fmt.Printf("OK, Selected! [Option]->%s [Path]->%s\n", optslct, pathslct)
		} else {
			helpcheck("<path check> This is not folder!\n")
		}
	default:
		helpcheck("<args check> Over Args [FileChain Program] [Option] [Just one folder Path to hash]")
	}

	switch optslct { //run
	case "new":
		fc := fchainew(pathslct)
		filechainwrite(pathslct, fc)
	case "update":
		fc := fchainud(pathslct)
		filechainwrite(pathslct, fc)
	case "verify":
		fchainvf(pathslct)
	}
	endtime := time.Since(starttime)
	fmt.Printf("\n실행시간: %s\n", endtime)
}

func fchainvf(path string) {
	var dfstr string
	var dfstrlen int
	var dfhash [64]byte
	check := 0
	var dfes []string
	alldf := allDFfind(path) //폴더안 모든 폴더와 파일경로 검색
	alldflen := len(alldf)
	finalhash := make([]byte, 128) //폴더안 .filechain 값 저장
	for i := 0; i < alldflen; i++ {
		dirfiles, err := os.Open(alldf[i])
		defer dirfiles.Close()
		errcheck(err, "<fchainvf> Can't open file or folder")
		dfstat, err := dirfiles.Stat()
		errcheck(err, "<fchainvf> Can't open file or folder stat")
		dfstr = dfstat.Name()
		dfstrlen = len(dfstr)
		if dfstrlen > 10 && dfstr[dfstrlen-10:] == ".filechain" {
			check++
			_, err := dirfiles.Read(finalhash)
			errcheck(err, "<fchainvf> Can't read *.filechain file")
			continue
		}
		if !dfstat.IsDir() {
			dfstr += fmt.Sprint(dfstat.Size())
			dfstr += fmt.Sprint(dfstat.ModTime().Format("2006-01-02 15:04:05"))
		}
		dfes = append(dfes, dfstr)
	}
	if check > 1 {
		panic("<fchainvf> Why are there more than 2 *.filechain?")
	} else if check == 1 {
		dfeslen := len(dfes)
		for i := 0; i < dfeslen; i++ {
			dfhash = blake2b.Sum512([]byte(dfes[i]))
			for p := 0; p < 64; p++ { //xor로 이전파일체인값 검색 가능
				finalhash[p] ^= dfhash[p]
			}
		}
		truecheck := true
		for t := 0; t < 64; t++ {
			if finalhash[t] != finalhash[t+64] {
				truecheck = false
				println("[verify] -> Flase")
				break
			}
		}
		if truecheck {
			println("[verify] -> True")
		}
	} else {
		panic("<fchainvf> Where is *.filechain?")
	}
}

func fchainud(path string) []byte {
	var dfstr string
	var dfstrlen int
	var dfhash [64]byte
	check := 0
	var dfes []string
	alldf := allDFfind(path) //폴더안 모든 폴더와 파일경로 검색
	alldflen := len(alldf)
	finalhash := make([]byte, 128) //현제 .filechain 값 저장
	for i := 0; i < alldflen; i++ {
		dirfiles, err := os.Open(alldf[i])
		defer dirfiles.Close()
		errcheck(err, "<fchainud> Can't open file or folder")
		dfstat, err := dirfiles.Stat()
		errcheck(err, "<Fchainud> Can't open file or folder stat")
		dfstr = dfstat.Name()
		dfstrlen = len(dfstr)
		if dfstrlen > 10 && dfstr[dfstrlen-10:] == ".filechain" {
			check++
			_, err := dirfiles.Read(finalhash)
			errcheck(err, "<fchainud> Can't read *.filechain file")
			continue
		}
		if !dfstat.IsDir() {
			dfstr += fmt.Sprint(dfstat.Size())
			dfstr += fmt.Sprint(dfstat.ModTime().Format("2006-01-02 15:04:05"))
		}
		dfes = append(dfes, dfstr)
	}
	if check > 1 {
		panic("<Fchainud> Why are there more than 2 *.filechain?")
	} else if check == 1 {
		for m := 0; m < 64; m++ { //현제해시를 이전해시에 덮어쓰기
			finalhash[m+64] = finalhash[m]
		}
		dfeslen := len(dfes)
		for i := 0; i < dfeslen; i++ {
			dfhash = blake2b.Sum512([]byte(dfes[i]))
			for p := 0; p < 64; p++ { //xor로 이전파일체인값 검색 가능
				finalhash[p] ^= dfhash[p]
			}
		}
	} else {
		panic("<Fchainud> Where is *.filechain?")
	}
	return finalhash
}

func fchainew(path string) []byte {
	var dfstr string
	var dfstrlen int
	var dfhash [64]byte
	alldf := allDFfind(path) //폴더안 모든 폴더와 파일경로 검색
	alldflen := len(alldf)
	finalhash := make([]byte, 128) //64byte길이의 초기값 2번 반복해서 입력
	for i := 0; i < alldflen; i++ {
		dirfiles, err := os.Open(alldf[i])
		defer dirfiles.Close()
		errcheck(err, "<fchainew> Can't open file or folder")
		dfstat, err := dirfiles.Stat()
		errcheck(err, "<fchainew> Can't open file or folder stat")
		dfstr = dfstat.Name()
		dfstrlen = len(dfstr)
		if dfstrlen > 10 && dfstr[dfstrlen-10:] == ".filechain" {
			panic("<fchainew> Remove *.filechain file plz")
		}
		if !dfstat.IsDir() {
			dfstr += fmt.Sprint(dfstat.Size())
			dfstr += fmt.Sprint(dfstat.ModTime().Format("2006-01-02 15:04:05"))
		}
		dfhash = blake2b.Sum512([]byte(dfstr))
		for p := 0; p < 64; p++ { //xor로 이전파일체인값 검색 가능
			finalhash[p] ^= dfhash[p]
		}
	}
	return finalhash
}

func filechainwrite(path string, hashvalue []byte) {
	nf, err := os.Create(path + "\\a.filechain") //대상폴더안 파일체인명
	defer nf.Close()
	errcheck(err, "<filechainwrite> Can not create file")
	_, err = nf.Write(hashvalue)
	errcheck(err, "<filechainwrite> Can not write file")
}

func allDFfind(dirlocation string) []string {
	dfinfo := make([]string, 0)
	filepath.Walk(dirlocation, func(path string, info os.FileInfo, err error) error {
		dfinfo = append(dfinfo, path)
		return nil
	})
	return dfinfo
}

func errcheck(e error, s string) {
	if e != nil {
		println(s, "\n")
		os.Exit(1)
	}
}

func helpcheck(s string) {
	println(s, "\nYou can [FileChain Program] [help]\n")
	os.Exit(1)
}
