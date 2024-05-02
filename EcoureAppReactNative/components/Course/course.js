import { ActivityIndicator, Alert, Image, ScrollView, StyleSheet, Text, View } from "react-native"
import stylesSheet from "../../Styles/stylesSheet"
import React from 'react';
import API, { endpoint } from "../../config/API";
import { Chip, List, Searchbar } from "react-native-paper";

const Course =()=>{
    const [cat,setCat]= React.useState(null);
    const [course,setcourse]=React.useState([]);
    const[load,setLoad]=React.useState(false);
    const[q,setQ]=React.useState("");
    const [cateId, setCateId] = React.useState("");
    const loadCat= async() =>{
        try{
            let ds= await API.get(endpoint['category'])
            setCat(ds.data);
            console.log(ds.data);
        }catch(ex)
        {
            console.error(ex);
        }
        
    }
    const loadCourse=async()=>{
        try{
            setLoad(true)
            let url=`${endpoint['course']}?q=${q}&category_id=${cateId}`;
            let getCourse= await API.get(url);
            setcourse(getCourse.data.results);
            console.log(getCourse.data.results);
        }catch(ex)
        {
            console.error(ex);
        }
        finally{
            setLoad(false)
        }

    }
    
     React.useEffect(()=>{
         loadCat()
     },[])
     React.useEffect(()=>{
        loadCourse()
    },[q,cateId])
    return(
        <View style={stylesSheet.container}>
            <Text style={stylesSheet.course}>Course</Text>
            <View style={[stylesSheet.row,stylesSheet.wrap]}>
             <Chip mode={cateId?"flat":"outlined"} style={stylesSheet.margin} icon="tag" onPress={() => setCateId("")}>Tất cả</Chip>
                {cat===null?<ActivityIndicator/>:<>
                {cat.map(c=>
                <Chip icon="tag" style={stylesSheet.margin} key={c.id} onPress={() => setCateId(c.id)}>{c.name} </Chip>)}
                </>}
            </View>
            <View>
                <Searchbar placeholder="Nhap ten khoa hoc,,,," value={q} onChangeText={setQ}></Searchbar>
            </View>
            <ScrollView>
                {load && <ActivityIndicator/>}
                {course.map(c => <List.Item key={c.id} title={c.subject} description={c.created_date} 
                                             left={() => <Image style={stylesSheet.avatar} source={{uri: c.image}} />} />)}
            </ScrollView>
        </View>
        
    )
}
export default Course