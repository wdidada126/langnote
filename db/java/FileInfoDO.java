package com.xxxx.media.image.extraction.dal.models;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.serializer.SerializerFeature;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author DuanRan
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FileInfoDO implements Serializable {

  private Long id;

  private String groupId;

  private String fileId;

  private String fileName;

  private String createdBy;

  private Date createdAt;

  private String updatedBy;

  private Date updatedAt;

  private String tableName;

  private static final long serialVersionUID = -7985878305256458565L;

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append(getClass().getSimpleName());
    sb.append(" [");
    sb.append("Hash = ").append(hashCode());
    sb.append(", id=").append(id);
    sb.append(", groupId=").append(groupId);
    sb.append(", fileId=").append(fileId);
    sb.append(", fileName=").append(fileName);
    sb.append(", createdBy=").append(createdBy);
    sb.append(", createdAt=").append(createdAt);
    sb.append(", updatedBy=").append(updatedBy);
    sb.append(", updatedAt=").append(updatedAt);
    sb.append("]");
    return sb.toString();
  }
}