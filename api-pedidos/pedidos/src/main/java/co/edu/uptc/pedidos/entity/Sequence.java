package co.edu.uptc.pedidos.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Document(collection = "sequences")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Sequence {
	
    @Id
    private String id;
    private Long seq;
    
    public Long getSeq() {
        return this.seq;
    }
    
    public void setSeq(Long seq) {
        this.seq = seq;
    }
}
